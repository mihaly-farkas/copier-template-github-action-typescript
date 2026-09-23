from pathlib import Path
from rich import print

from agent.conf import PROJECT_ROOT, REFERENCE_PROJECT_DIR, REFERENCE_PROJECT_GIT_DIFF_PATH
from spec.lib.run_command import run_command


def git_diff_reference_project() -> Path:
  print("[dim]Creating git diff of the reference project...[/dim]")
  run_command(PROJECT_ROOT, f"git diff HEAD {REFERENCE_PROJECT_DIR} > {REFERENCE_PROJECT_GIT_DIFF_PATH}")
  return REFERENCE_PROJECT_GIT_DIFF_PATH
