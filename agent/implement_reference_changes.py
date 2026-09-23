#!/usr/bin/env python3

import argparse
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from rich import print

from node.final_step_placeholder import final_step_placeholder
from node.implement_changes import implement_changes
from node.post_check import post_check
from node.pre_check import pre_check
from node.start import start
from router.post_check_router import post_check_router
from router.pre_check_router import pre_check_router
from state.workflow_state import WorkflowState

# ============================================================================

workflow = StateGraph(WorkflowState)

workflow.add_node("start", start)
workflow.add_node("pre_check", pre_check)
workflow.add_node("call_llm", implement_changes)
workflow.add_node("post_check", post_check)
workflow.add_node("final_step", final_step_placeholder)

# ============================================================================

workflow.set_entry_point("start")
workflow.add_edge("start", "pre_check")
workflow.add_conditional_edges(
  "pre_check",
  pre_check_router,
  {
    "start_loop": "call_llm",
    "abort": END,
  },
)
workflow.add_edge("call_llm", "post_check")
workflow.add_conditional_edges(
  "post_check",
  post_check_router,
  {
    "retry": "call_llm",
    "next_step": "final_step",
    "abort": END,
  },
)
workflow.add_edge("final_step", END)

# ============================================================================

app = workflow.compile()

if __name__ == "__main__":
  description = "Software Factory :: Copier Template :: GitHub Action :: TypeScript :: Implement Reference Changes"
  print(f"[cyan]{description}[/cyan]")

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument(
    "--max-attempts",
    type=int,
    default=1,
    help="Maximum number of attempts for the workflow"
  )
  args = parser.parse_args()

  load_dotenv()

  app.invoke(
    {
      "max_attempts": args.max_attempts,
    }
  )
