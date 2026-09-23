import pytest
from pathlib import Path
from typing import TypedDict

from .conftest import PROJECT_ROOT, TMP_DIR
from .lib.compare_files import compare_files
from .lib.generate_project import generate_project
from .lib.run_command import run_command
from .lib.template_parameters import TemplateParameters


class SpecCase(TypedDict):
  id: str
  template_parameters: TemplateParameters


SPEC_CASES = [
  {
    "id": "reference-project-01",
    "template_parameters": {
      "licenseOwner": "DYNAMIC_TOKEN:9c3774360",
      "githubRepositoryOwner": "dynamic-token-0a9c1842",
      "githubRepositoryName": "dynamic-token-aa9d4c88",
      "githubActionName": "DYNAMIC_TOKEN:1fe1a5f3",
      "githubActionNameCamelCase": "dynamicToken1fe1a5f3",
      "githubActionNameKebabCase": "dynamic-token-1fe1a5f3",
      "githubActionDescription": "DYNAMIC_TOKEN:19bd01a9",
      "githubActionExampleStepName": "DYNAMIC_TOKEN:77ad0c5e",
      "licenseYearStart": 896,
    },
  },
  {
    "id": "reference-project-02",
    "template_parameters": {
      "licenseOwner": "Jane Doe",
      "githubRepositoryOwner": "jane-doe",
      "githubRepositoryName": "github-action-reference-02",
      "githubActionName": "Custom Action 02",
      "githubActionNameCamelCase": "customAction02",
      "githubActionNameKebabCase": "custom-action-02",
      "githubActionDescription": "This is yet another dummy GitHub Action that does nothing",
      "githubActionExampleStepName": "Do something other interesting",
    },
  },
  {
    "id": "reference-project-03",
    "template_parameters": {
      "licenseOwner": "John Doe",
      "githubRepositoryOwner": "john-doe",
      "githubRepositoryName": "github-action-reference-03",
      "githubActionName": "Custom Action 03",
      "githubActionNameCamelCase": "customAction03",
      "githubActionNameKebabCase": "custom-action-03",
      "githubActionDescription": "This is a dummy GitHub Action that does nothing",
      "githubActionExampleStepName": "Do something interesting",
    },
  },
]

IGNORE_PATTERNS = [
  r"\.idea/.*",
  r"build/.*",
  r"coverage/.*",
  r"node_modules/.*",
  r".*\.iml",
  r"package-lock\.json",
]


@pytest.mark.parametrize("spec", SPEC_CASES)
def test_project_can_be_generated_with_default_parameters(spec) -> None:
  # ARRANGE
  target_dir = TMP_DIR / spec["id"]
  params = spec["template_parameters"]
  # ACT
  result = generate_project(target_dir, params)
  # ASSERT
  assert result.error is None, result


@pytest.mark.parametrize("spec", SPEC_CASES)
def test_generated_project_can_install_npm_dependencies(spec) -> None:
  # ARRANGE
  target_dir = TMP_DIR / spec["id"]
  # ACT
  result = run_command(target_dir, "npm install")
  # ASSERT
  assert result.error is None, result


@pytest.mark.parametrize("spec", SPEC_CASES)
def test_generated_project_can_run_tests(spec) -> None:
  # ARRANGE
  target_dir = TMP_DIR / spec["id"]
  # ACT
  result = run_command(target_dir, "npm run test")
  # ASSERT
  assert result.error is None, result


@pytest.mark.parametrize("spec", SPEC_CASES)
def test_generated_project_matches_reference(spec) -> None:
  # ARRANGE
  target_dir = TMP_DIR / spec["id"]
  reference_dir = PROJECT_ROOT / "assert" / spec["id"]
  # ACT
  differences = compare_files(
    target_dir,
    reference_dir,
    IGNORE_PATTERNS,
  )
  # ASSERT
  assert differences["number_of_differences"] == 0, differences
