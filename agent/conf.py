import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = PROJECT_ROOT / ".tmp"
AI_WORKSPACE_DIR = PROJECT_ROOT / ".ai-workspace"
AI_ARCHIVE_DIR = PROJECT_ROOT / ".ai-archive"
REFERENCE_PROJECT_DIR = PROJECT_ROOT / "assert" / "reference-project-01"
REFERENCE_PROJECT_GIT_DIFF_PATH = AI_WORKSPACE_DIR / "git_diff.reference.patch"
TEMPLATE_DIR = PROJECT_ROOT / "template"
TEMPLATE_GIT_DIFF_PATH = AI_WORKSPACE_DIR / "git_diff.template.patch"
WORKFLOW_STATE_JSON_PATH = AI_WORKSPACE_DIR / "state.json"

if str(PROJECT_ROOT) not in sys.path:
  sys.path.insert(0, str(PROJECT_ROOT))
