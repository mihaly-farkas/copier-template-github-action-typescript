import pytest
from pathlib import Path

from .conftest import TMP_DIR
from .lib.generate_project import generate_project


@pytest.mark.parametrize("license_year_start", [2022, 2023, 2024])
def test_generated_license_includes_configured_start_year(license_year_start: int) -> None:
  #ARRANGE
  dir = TMP_DIR / f"license-year-start-project-{license_year_start}"
  license_file = dir / "LICENSE"
  params = {
    "licenseOwner": "My Name",
    "licenseYearStart": license_year_start,
    "githubRepositoryOwner": "my-github-username",
    "githubRepositoryName": "my-repo-name",
    "githubActionName": "My Action",
    "githubActionNameCamelCase": "myAction",
    "githubActionNameKebabCase": "my-action",
    "githubActionDescription": "This is my GitHub Action",
    "githubActionExampleStepName": "Do something",
  }
  # ACT
  result = generate_project(dir, params)
  # ASSERT
  assert result.error is None, result
  assert f"Copyright (c) {license_year_start}-2026 My Name" in license_file.read_text()
