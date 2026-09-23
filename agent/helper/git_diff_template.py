from pathlib import Path
from rich import print

from agent.conf import PROJECT_ROOT, TEMPLATE_DIR, TEMPLATE_GIT_DIFF_PATH
from spec.lib.run_command import run_command


def git_diff_template() -> Path:
  print("[dim]Creating git diff of the template dir...[/dim]")
  run_command(PROJECT_ROOT, f"git diff HEAD {TEMPLATE_DIR} > {TEMPLATE_GIT_DIFF_PATH}")
  return TEMPLATE_GIT_DIFF_PATH
