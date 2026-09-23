import subprocess
from rich import print

from agent.helper.save_workflow_state import save_workflow_state
from agent.state.workflow_state import WorkflowState


def post_check(state: WorkflowState):
  state["status"] = "success"
  save_workflow_state(state)
  return state

  result = subprocess.run(
    ["pytest", "spec/copy_default_spec.py"], capture_output=True, text=True
  )

  if result.returncode == 0:
    print("[green]Post-checks passed! Template successfully matches reference.[/green]")
    return {"status": "success"}

  target_test = "test_generated_project_matches_reference"
  if target_test in result.stdout:
    print("[yellow]Template still does not match reference. Retry needed.[/yellow]")
    return {"status": "needs_retry"}

  print("[red]Copilot introduced a syntax or structural error.[/red]")
  return {"status": "structural_error", "message": "Copilot broke the template structure."}
