#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from rich import print

sys.path.insert(0, str(Path(__file__).parent))
from lib.price_estimation import build_price_estimation_report

SOURCE_DATA_FILE_PATH = ".ai-archive/ai-workspace.20260924_201430/state.json"
GITHUB_COPILOT_PRICE_TABLE_JSON_PATH = ".data-analitics/github-copilot.price-table.json"
PRICE_ESTIMATION_REPORT_JSON_PATH = ".data-analitics/github-copilot.price-estimation-report.json"
PRICE_ESTIMATION_REPORT_MD_PATH = ".data-analitics/github-copilot.price-estimation-report.md"

result = build_price_estimation_report(SOURCE_DATA_FILE_PATH, GITHUB_COPILOT_PRICE_TABLE_JSON_PATH)
sorted_price_estimation = result["price_estimation"]
total_input_tokens = result["input"] + result["cached_input"]

print(f"[green]Estimated cost across {len(sorted_price_estimation)} models based on "
      f"{total_input_tokens} input tokens and {result['output']} output tokens[/green]")

Path(PRICE_ESTIMATION_REPORT_JSON_PATH).write_text(
    json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
print(f"[dim]Saved JSON report to {PRICE_ESTIMATION_REPORT_JSON_PATH}[/dim]")

md_lines = [
    "# GitHub Copilot Price Estimation Report",
    "",
    "This report estimates the cost of the recorded AI workflow run if it had been "
    "executed with each available GitHub Copilot model. Token usage (input, cached "
    "input, cache write, and output) is extracted from the workflow's AI messages, "
    "then priced per model using the official GitHub Copilot price table (prices are "
    "quoted per 1M tokens). The `ai_credit` column converts the total cost into "
    "GitHub Copilot AI Credits (1 AI Credit = $0.01 USD). The `multiplier` column "
    "shows how much more expensive a model is compared to the cheapest option, "
    "which is always `1.0`.",
    "",
    f"- Input tokens: **{result['input']}**",
    f"- Cached input tokens: **{result['cached_input']}**",
    f"- Cache write tokens: **{result['cache_write']}**",
    f"- Output tokens: **{result['output']}**",
    "",
    "## Price Estimation",
    "",
    "| Model | Input ($) | Cached input ($) | Cache write ($) | Output ($) | Total ($) | AI Credit | Multiplier |",
    "|---|---:|---:|---:|---:|---:|---:|---:|",
]
for entry in sorted_price_estimation:
    md_lines.append(
        f"| {entry['model']} | {entry['input']:.6f} | {entry['cached_input']:.6f} | "
        f"{entry['cache_write']:.6f} | {entry['output']:.6f} | {entry['total']:.6f} | "
        f"{entry['ai_credit']:.4f} | {entry['multiplier']:.2f}x |"
    )
md_lines.append("")

Path(PRICE_ESTIMATION_REPORT_MD_PATH).write_text("\n".join(md_lines), encoding="utf-8")
print(f"[dim]Saved Markdown report to {PRICE_ESTIMATION_REPORT_MD_PATH}[/dim]")
