def pre_check_router(state: dict) -> str:
  if state["status"] == "needs_implementation":
    return "start_loop"
  return "abort"
