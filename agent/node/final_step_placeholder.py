import shutil
from datetime import datetime
from helper.save_workflow_state import save_workflow_state
from state.workflow_state import WorkflowState

from agent.conf import PROJECT_ROOT, AI_ARCHIVE_DIR, AI_WORKSPACE_DIR, REFERENCE_PROJECT_DIR, TEMPLATE_DIR
from agent.helper.git_diff_template import git_diff_template
from agent.helper.print_separator import print_separator
from spec.lib.run_command import run_command
from rich import print

def final_step_placeholder(state: WorkflowState):
  print_separator("complete")

  git_diff_template()

  state["status"] = "completed"
  save_workflow_state(state)

  AI_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  archive_path = AI_ARCHIVE_DIR / f"ai-workspace.{timestamp}/"

  print("[dim]Archiving AI workspace...[/dim]")
  shutil.copytree(AI_WORKSPACE_DIR, archive_path)

  print(f"[dim]Adding {archive_path} to git...[/dim]")
  run_command(PROJECT_ROOT, f"git add {archive_path}")

  print(f"[dim]Adding {REFERENCE_PROJECT_DIR} to git...[/dim]")
  run_command(PROJECT_ROOT, f"git add {REFERENCE_PROJECT_DIR} -A")

  print(f"[dim]Adding {TEMPLATE_DIR} to git...[/dim]")
  run_command(PROJECT_ROOT, f"git add {TEMPLATE_DIR} -A")

  return state
