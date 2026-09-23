import os
from rich import print


def print_separator(text, color="yellow", char="="):
  width = os.get_terminal_size().columns
  line = f" {text} ".center(width, char)
  print(f"[{color}]{line}[/{color}]")
