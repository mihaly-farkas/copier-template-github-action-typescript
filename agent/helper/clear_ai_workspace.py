import shutil

from agent.conf import AI_WORKSPACE_DIR


def clear_ai_workspace():
  shutil.rmtree(AI_WORKSPACE_DIR, ignore_errors=True)
  AI_WORKSPACE_DIR.mkdir(parents=True)
