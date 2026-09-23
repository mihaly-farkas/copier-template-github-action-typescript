import sys
from pathlib import Path
from typing import Optional, TypedDict, List

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
  sys.path.insert(0, project_root)

from spec.lib.compare_files import CompareFilesResult


class WorkflowState(TypedDict):
  status: str
  message: Optional[str]
  attempts: int
  max_attempts: int
  compare_files_result: CompareFilesResult
  workflow_history: List[dict]
