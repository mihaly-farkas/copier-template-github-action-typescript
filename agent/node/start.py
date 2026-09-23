from helper.print_separator import print_separator
from state.workflow_state import WorkflowState

from agent.helper.clear_ai_workspace import clear_ai_workspace
from agent.helper.save_workflow_state import save_workflow_state


def start(state: WorkflowState):
  clear_ai_workspace()

  state["status"] = "started"
  state["attempts"] = 0
  state["workflow_history"] = []
  save_workflow_state(state)
  return state
