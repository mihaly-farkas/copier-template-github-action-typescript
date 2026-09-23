# import os
# import re
# import subprocess
# from datetime import datetime
# from helper.print_separator import print_separator
# from langchain.agents import create_agent
# from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
# from langchain_githubcopilot_chat import ChatGithubCopilot
# from pathlib import Path
# from rich import print

from agent.helper.invoke_llm_agent import invoke_llm_agent
from agent.helper.save_workflow_state import save_workflow_state
from agent.state.workflow_state import WorkflowState
from agent.tool.execute_bash_command import execute_bash_command

SKILL_PATH = ".github/skills/implement-reference-changes/SKILL.md"
DEFAULT_LLM_MODEL = "gpt-4o"
DEFAULT_LLM_TEMPERATURE = 0.2
TOOLS = [execute_bash_command]


def implement_changes(state: WorkflowState):
  current_attempt = state.get("attempts", 0) + 1

  llm_model = DEFAULT_LLM_MODEL
  llm_temperature = DEFAULT_LLM_TEMPERATURE

  llm_prompt = "Modify the _Template Blueprint_ to implement the changes in the _Reference Project_."

  event = invoke_llm_agent(
    {
      "node": "implement_changes",
      "model": llm_model,
      "temperature": llm_temperature,
      "prompt": llm_prompt,
      "skill": SKILL_PATH,
      "tools": TOOLS
    }
  )
  state["status"] = "template_updated"
  state["attempts"] = current_attempt
  state["workflow_history"].append(event)
  save_workflow_state(state)
  return state
