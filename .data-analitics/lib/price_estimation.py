#!/usr/bin/env python3
"""Reusable data loading/transformation helpers for GitHub Copilot price estimation."""

import json
from pathlib import Path

AI_CREDIT_USD = 0.01


def extract_token_usage(message: dict) -> dict:
    """Extracts the input / cached_input / cache_write / output token counts
    from a single "ai" message, using response_metadata.token_usage as the
    primary source and falling back to usage_metadata when needed."""
    token_usage = message.get("response_metadata", {}).get("token_usage", {}) or {}
    prompt_tokens_details = token_usage.get("prompt_tokens_details", {}) or {}
    usage_metadata = message.get("usage_metadata", {}) or {}
    input_token_details = usage_metadata.get("input_token_details", {}) or {}

    prompt_tokens = token_usage.get("prompt_tokens", 0) or 0
    cached_input = prompt_tokens_details.get("cached_tokens")
    if cached_input is None:
        cached_input = input_token_details.get("cache_read", 0) or 0

    cache_write = prompt_tokens_details.get("cache_write_tokens", 0) or 0

    output = token_usage.get("completion_tokens")
    if output is None:
        output = usage_metadata.get("output_tokens", 0) or 0

    return {
        "input": prompt_tokens - cached_input,
        "cached_input": cached_input,
        "cache_write": cache_write,
        "output": output,
    }


def select_price_entry(entries: list[dict], total_input_tokens: int) -> dict:
    """Picks the tier whose threshold (inclusive upper bound) covers the total
    input token volume; falls back to the unbounded (threshold None) tier."""
    bounded = sorted(
        (entry for entry in entries if entry["input_token_threshold"] is not None),
        key=lambda entry: entry["input_token_threshold"],
    )
    for entry in bounded:
        if total_input_tokens <= entry["input_token_threshold"]:
            return entry

    unbounded = next((entry for entry in entries if entry["input_token_threshold"] is None), None)
    return unbounded if unbounded is not None else entries[-1]


def build_price_estimation_report(source_data_file_path: str, price_table_json_path: str) -> dict:
    """Loads the workflow history and the price table, then builds the full
    price estimation report structure (token usage details + per-model cost
    estimation), ready to be serialized (e.g. to JSON or Markdown)."""
    data = json.loads(Path(source_data_file_path).read_text(encoding="utf-8"))
    messages = data["workflow_history"][0]["response"]["messages"]

    ai_messages = [message for message in messages if message["type"] == "ai"]

    transformed_messages = [
        {
            "tool_call": bool(message.get("tool_calls")),
            "response": not bool(message.get("tool_calls")),
            **extract_token_usage(message),
        }
        for message in ai_messages
    ]

    result = {
        "input": sum(message["input"] for message in transformed_messages),
        "cached_input": sum(message["cached_input"] for message in transformed_messages),
        "cache_write": sum(message["cache_write"] for message in transformed_messages),
        "output": sum(message["output"] for message in transformed_messages),
        "details": transformed_messages,
    }

    price_table = json.loads(Path(price_table_json_path).read_text(encoding="utf-8"))

    # Total input volume (fresh + cached) used to decide which pricing tier (threshold) applies.
    total_input_tokens = result["input"] + result["cached_input"]

    # Group price table rows by model, since a model can have multiple tiers
    # (e.g. "Default" up to a threshold, and "Long context" above it).
    price_entries_by_model: dict[str, list[dict]] = {}
    for entry in price_table:
        price_entries_by_model.setdefault(entry["model"], []).append(entry)

    price_estimation = []
    for model_name, entries in price_entries_by_model.items():
        price_entry = select_price_entry(entries, total_input_tokens)

        input_cost = (result["input"] / 1_000_000) * price_entry["input"]
        cached_input_cost = (result["cached_input"] / 1_000_000) * price_entry["cached_input"]
        cache_write_cost = (result["cache_write"] / 1_000_000) * price_entry["cache_write"]
        output_cost = (result["output"] / 1_000_000) * price_entry["output"]
        total_cost = input_cost + cached_input_cost + cache_write_cost + output_cost

        price_estimation.append(
            {
                "model": model_name,
                "input": input_cost,
                "cached_input": cached_input_cost,
                "cache_write": cache_write_cost,
                "output": output_cost,
                "total": total_cost,
                "ai_credit": total_cost / AI_CREDIT_USD,
            }
        )

    sorted_price_estimation = sorted(price_estimation, key=lambda entry: entry["total"])
    cheapest_total = sorted_price_estimation[0]["total"]
    for entry in sorted_price_estimation:
        entry["multiplier"] = entry["total"] / cheapest_total

    result["price_estimation"] = sorted_price_estimation

    return result
