from pathlib import Path

from .conftest import PROJECT_ROOT, TMP_DIR
from .lib.compare_files import compare_files
from .lib.generate_project import generate_project
from .lib.run_command import run_command
from .lib.template_parameters import get_default_template_parameters

DEFAULT_CASE = "default-project"
IGNORE_PATTERNS = [
  r"\.idea/.*",
  r"build/.*",
  r"coverage/.*",
  r"node_modules/.*",
  r".*\.iml",
  r"package-lock\.json",
]


def project_dir(case: str) -> Path:
  return TMP_DIR / case


def test_project_can_be_generated_with_default_parameters() -> None:
  result = generate_project(project_dir(DEFAULT_CASE), get_default_template_parameters())
  assert result.error is None, result


def test_generated_project_can_install_npm_dependencies() -> None:
  result = run_command(str(project_dir(DEFAULT_CASE)), "npm install")
  assert result.error is None, result


def test_generated_project_can_run_tests() -> None:
  result = run_command(str(project_dir(DEFAULT_CASE)), "npm run test")
  assert result.error is None, result


def test_generated_project_matches_reference() -> None:
  differences = compare_files(
    project_dir(DEFAULT_CASE),
    PROJECT_ROOT / "assert" / DEFAULT_CASE,
    IGNORE_PATTERNS,
  )
  assert not differences, "\n".join(differences)
