import re
from pathlib import Path
from typing import Callable, List, Optional, Union, TypedDict


class CompareFilesResult(TypedDict):
  number_of_differences: int
  missing_files: List[str]
  changed_files: List[str]
  unexpected_files: List[str]


def visit_files(
  base_dir: Union[str, Path], ignore_patterns: List, callback: Callable[[str], None]
) -> None:
  base_path = Path(base_dir).resolve()
  for file_path in sorted(path for path in base_path.rglob("*") if path.is_file()):
    relative_path = file_path.relative_to(base_path).as_posix()
    if not any(re.search(pattern, relative_path) for pattern in ignore_patterns):
      callback(relative_path)


def compare_files(
  actual_dir: Union[str, Path],
  expected_dir: Union[str, Path],
  ignore_patterns: Optional[List] = None,
) -> CompareFilesResult:
  ignored = ignore_patterns or []
  actual_path = Path(actual_dir).resolve()
  expected_path = Path(expected_dir).resolve()
  result: CompareFilesResult = {
    "number_of_differences": 0,
    "missing_files": [],
    "changed_files": [],
    "unexpected_files": [],
  }

  def compare(relative_path: str) -> None:
    actual_file = actual_path / relative_path
    expected_file = expected_path / relative_path
    if not actual_file.exists():
      result["missing_files"].append(relative_path)
      result["number_of_differences"] += 1
    elif actual_file.read_text() != expected_file.read_text():
      result["changed_files"].append(relative_path)
      result["number_of_differences"] += 1

  visit_files(expected_path, ignored, compare)

  def find_unexpected(relative_path: str) -> None:
    if not (expected_path / relative_path).exists():
      result["unexpected_files"].append(relative_path)
      result["number_of_differences"] += 1

  visit_files(actual_path, ignored, find_unexpected)

  return result
