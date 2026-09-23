import re
from pathlib import Path
from typing import Callable, List, Optional, Union


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
) -> List:
  ignored = ignore_patterns or []
  actual_path = Path(actual_dir).resolve()
  expected_path = Path(expected_dir).resolve()
  differences: List = []

  def compare(relative_path: str) -> None:
    actual_file = actual_path / relative_path
    expected_file = expected_path / relative_path
    if not actual_file.exists():
      differences.append(f"Missing generated file: {relative_path}")
    elif actual_file.read_text() != expected_file.read_text():
      differences.append(f"File contents differ: {relative_path}")

  visit_files(expected_path, ignored, compare)

  def find_unexpected(relative_path: str) -> None:
    if not (expected_path / relative_path).exists():
      differences.append(f"Unexpected generated file: {relative_path}")

  visit_files(actual_path, ignored, find_unexpected)
  return differences
