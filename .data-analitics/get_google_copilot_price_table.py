#!/usr/bin/env python3

import json
from html.parser import HTMLParser
from pathlib import Path
from typing import TypedDict

import requests
from rich import print

GITHUB_COPILOT_PRICE_TABLE_HTML_URL = "https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing"
GITHUB_COPILOT_PRICE_TABLE_JSON_PATH = ".data-analitics/github-copilot.price-table.json"
TMP_DIR = ".data-analitics/.tmp"
TMP_HTML_PATH = f"{TMP_DIR}/github-copilot.price-table.html"

MODEL_MAPPING = {
  # --- OpenAI (GPT) ---
  'GPT-5 mini': {
    'model_id': 'gpt-5-mini',
    'model_kwargs': {}
  },
  'GPT-5.3-Codex': {
    'model_id': 'gpt-5.3-codex',
    'model_kwargs': {}
  },
  'GPT-5.4': {
    'model_id': 'gpt-5.4',
    'model_kwargs': {}
  },
  'GPT-5.4 mini': {
    'model_id': 'gpt-5.4-mini',
    'model_kwargs': {}
  },
  'GPT-5.4 nano': {
    'model_id': 'gpt-5-nano',
    'model_kwargs': {}
  },
  'GPT-5.5': {
    'model_id': 'gpt-5.5',
    'model_kwargs': {}
  },
  'GPT-5.6 Luna': {
    'model_id': 'gpt-5.6-luna',
    'model_kwargs': {}
  },
  'GPT-5.6 Sol': {
    'model_id': 'gpt-5.6-sol',
    'model_kwargs': {}
  },
  'GPT-5.6 Terra': {
    'model_id': 'gpt-5.6-terra',
    'model_kwargs': {}
  },
  'GPT-6 Astra': {
    'model_id': 'gpt-6-astra',
    'model_kwargs': {}
  },
  'GPT-6 Luna': {
    'model_id': 'gpt-6-luna',
    'model_kwargs': {}
  },
  'GPT-6 Sol': {
    'model_id': 'gpt-6-sol',
    'model_kwargs': {}
  },

  # --- Anthropic (Claude) ---
  'Claude Haiku 4.5': {
    'model_id': 'claude-haiku-4-5',
    'model_kwargs': {}
  },
  'Claude Sonnet 4': {
    'model_id': 'claude-sonnet-4',
    'model_kwargs': {}
  },
  'Claude Sonnet 4.6': {
    'model_id': 'claude-sonnet-4-6',
    'model_kwargs': {}
  },
  'Claude Sonnet 5': {
    'model_id': 'claude-sonnet-5',
    'model_kwargs': {}
  },
  'Claude Opus 4.7': {
    'model_id': 'claude-opus-4-7',
    'model_kwargs': {}
  },
  'Claude Opus 4.8': {
    'model_id': 'claude-opus-4-8',
    'model_kwargs': {}
  },
  'Claude Opus 4.8 (fast mode) (preview)': {
    'model_id': 'claude-opus-4-8',
    'model_kwargs': {'speed': 'fast'} # Külön paraméter a gyors módhoz
  },
  'Claude Opus 5': {
    'model_id': 'claude-opus-5',
    'model_kwargs': {}
  },
  'Claude Opus 5.5': {
    'model_id': 'claude-opus-5-5',
    'model_kwargs': {}
  },
  'Claude Fable 5': {
    'model_id': 'claude-fable-5',
    'model_kwargs': {}
  },
  'Claude Fable 5.1': {
    'model_id': 'claude-fable-5-1',
    'model_kwargs': {}
  },

  # --- Google (Gemini) ---
  'Gemini 3.5 Flash': {
    'model_id': 'gemini-flash-3.5',
    'model_kwargs': {}
  },
  'Gemini 3.6 Flash1': {
    'model_id': 'gemini-flash-3.6',
    'model_kwargs': {}
  },
  'Gemini 3.7 Flash1': {
    'model_id': 'gemini-flash-3.7',
    'model_kwargs': {}
  },
  'Gemini 3.8 Flash1': {
    'model_id': 'gemini-flash-3.8',
    'model_kwargs': {}
  },

  # --- xAI (Grok) ---
  'Grok 4.5': {
    'model_id': 'grok-4-5',
    'model_kwargs': {}
  },
  'Grok 4.6': {
    'model_id': 'grok-4-6',
    'model_kwargs': {}
  },
  'Grok 4.7': {
    'model_id': 'grok-4-7',
    'model_kwargs': {}
  },

  # --- Moonshot AI & Microsoft ---
  'Kimi K2.7 Code': {
    'model_id': 'kimi-k2.7-code',
    'model_kwargs': {}
  },
  'Kimi K3': {
    'model_id': 'kimi-k3',
    'model_kwargs': {}
  },
  'MAI-Code-1.1-Flash': {
    'model_id': 'mai-code-1.1-flash',
    'model_kwargs': {}
  }
}

# Column headers we care about, mapped to their TypedDict field names.
WANTED_COLUMNS = {
    "Model": "model",
    "Threshold (input tokens)": "input_token_threshold",
    "Input": "input",
    "Cached input": "cached_input",
    "Cache write": "cache_write",
    "Output": "output",
}


class ModelPriceEntry(TypedDict):
    model: str
    model_id: str | None
    model_kwargs: dict[str, object]
    input_token_threshold: int | None
    input: float
    cached_input: float
    cache_write: float
    output: float


def parse_price(raw: str) -> float:
    """Converts a price cell (e.g. "$0.25") into a float. "Not applicable" -> 0."""
    if raw == "Not applicable":
        return 0.0
    return float(raw.replace("$", "").replace(",", "").strip())


def parse_threshold(raw: str) -> int | None:
    """Converts a threshold cell into the upper bound (inclusive) it represents.

    "≤ 200K" -> 200000 (the tier is valid up to and including this many tokens).
    "> 200K" or "Not applicable" -> None (no upper bound / not applicable).
    """
    if not raw.startswith("≤"):
        return None
    number = raw.lstrip("≤").strip()
    multiplier = 1
    if number.endswith("K"):
        multiplier = 1_000
        number = number[:-1]
    elif number.endswith("M"):
        multiplier = 1_000_000
        number = number[:-1]
    return int(float(number) * multiplier)


class PriceTableParser(HTMLParser):
    """Extracts Model / Input / Cached input / Cache write / Output columns
    from every <table> element found in the GitHub Copilot pricing page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.entries: list[ModelPriceEntry] = []

        self._in_table = False
        self._in_head = False
        self._in_row = False
        self._in_cell = False
        self._cell_text = ""
        self._header_names: list[str] = []
        self._wanted_indices: dict[int, str] = {}
        self._row_cells: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            self._in_table = True
            self._header_names = []
            self._wanted_indices = {}
        elif tag == "thead" and self._in_table:
            self._in_head = True
        elif tag in ("tr",) and self._in_table:
            self._in_row = True
            self._row_cells = []
        elif tag in ("td", "th") and self._in_row:
            self._in_cell = True
            self._cell_text = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "table":
            self._in_table = False
        elif tag == "thead":
            self._in_head = False
        elif tag in ("td", "th") and self._in_cell:
            self._in_cell = False
            self._row_cells.append(self._cell_text.strip())
        elif tag == "tr" and self._in_row:
            self._in_row = False
            if self._in_head:
                self._header_names = self._row_cells
                self._wanted_indices = {
                    index: WANTED_COLUMNS[name]
                    for index, name in enumerate(self._header_names)
                    if name in WANTED_COLUMNS
                }
            elif self._wanted_indices:
                raw_entry: dict[str, str] = {field: "Not applicable" for field in WANTED_COLUMNS.values()}
                for index, field in self._wanted_indices.items():
                    if index < len(self._row_cells):
                        raw_entry[field] = self._row_cells[index]
                if raw_entry.get("model"):
                    model_name = raw_entry["model"]
                    mapping = MODEL_MAPPING.get(model_name, {})
                    entry: ModelPriceEntry = {
                        "model": model_name,
                        "model_id": mapping.get("model_id"),
                        "model_kwargs": mapping.get("model_kwargs", {}),
                        "input_token_threshold": parse_threshold(raw_entry["input_token_threshold"]),
                        "input": parse_price(raw_entry["input"]),
                        "cached_input": parse_price(raw_entry["cached_input"]),
                        "cache_write": parse_price(raw_entry["cache_write"]),
                        "output": parse_price(raw_entry["output"]),
                    }
                    self.entries.append(entry)

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._cell_text += data


print(f"[dim]Downloading HTML from {GITHUB_COPILOT_PRICE_TABLE_HTML_URL}...[/dim]")
response = requests.get(GITHUB_COPILOT_PRICE_TABLE_HTML_URL, timeout=30)
response.raise_for_status()

Path(TMP_DIR).mkdir(parents=True, exist_ok=True)
Path(TMP_HTML_PATH).write_text(response.text, encoding="utf-8")

print(f"[dim]Parsing HTML and extracting price table...[/dim]")
parser = PriceTableParser()
parser.feed(response.text)
price_table: list[ModelPriceEntry] = parser.entries

print(f"[green]Extracted {len(price_table)} price entries[/green]")

print(f"[dim]Saving price table to {GITHUB_COPILOT_PRICE_TABLE_JSON_PATH}...[/dim]")
Path(GITHUB_COPILOT_PRICE_TABLE_JSON_PATH).write_text(
    json.dumps(price_table, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)

print(f"[green]Saved price table to {GITHUB_COPILOT_PRICE_TABLE_JSON_PATH}[/green]")

