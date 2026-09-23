import pytest
from pathlib import Path

from .conftest import TMP_DIR
from .lib.generate_project import generate_project
from .lib.template_parameters import get_default_template_parameters


@pytest.mark.parametrize("license_year_start", [2022, 2023, 2024])
def test_generated_license_includes_configured_start_year(license_year_start: int) -> None:
  project_dir = TMP_DIR / f"license-year-start-project-{license_year_start}"
  params = get_default_template_parameters()
  params["licenseYearStart"] = license_year_start

  result = generate_project(project_dir, params)
  assert result.error is None, result
  license_content = (project_dir / "LICENSE").read_text()
  assert f"Copyright (c) {license_year_start}-2026 My Name" in license_content
