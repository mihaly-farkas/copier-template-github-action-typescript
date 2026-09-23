def post_check_router(state: dict) -> str:
  if state["status"] == "success":
    return "next_step"
  if state.get("attempts", 0) < state["max_attempts"]:
    return "retry"
  return "abort"
