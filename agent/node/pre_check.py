from rich import print

from agent.helper.git_diff_reference_project import git_diff_reference_project
from agent.helper.print_separator import print_separator
from agent.helper.save_workflow_state import save_workflow_state
from agent.state.workflow_state import WorkflowState


def pre_check(state: WorkflowState):
  print_separator("Pre-check")

  git_diff = git_diff_reference_project()

  # If there are no differences, it means the reference templates do not
  # contain changes, so cancel the workflow
  if not git_diff.exists() or git_diff.stat().st_size == 0:
    print("[yellow]The Reference Templates do not contain changes[/yellow]")
    print("[yellow]Workflow cancelled[/yellow]")
    return {
      "status": "cancelled",
      "message": "The Reference Templates do not contain changes"
    }

  state["status"] = "needs_implementation"
  save_workflow_state(state)
  return state
