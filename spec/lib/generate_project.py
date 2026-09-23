import re
import shlex
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Union

from .run_command import CommandResult, run_command
from .template_parameters import TemplateParameters

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def generate_project(project_dir: Union[str, Path], params: TemplateParameters) -> CommandResult:
  project_path = Path(project_dir).resolve()
  project_path.parent.mkdir(parents=True, exist_ok=True)

  saved_node_modules: Optional[Path] = None
  node_modules = project_path / "node_modules"
  if node_modules.is_dir():
    tmp_dir = Path(tempfile.mkdtemp(prefix="copier-"))
    saved_node_modules = tmp_dir / "node_modules"
    node_modules.rename(saved_node_modules)

  shutil.rmtree(project_path, ignore_errors=True)
  command = ["copier", "copy", ".", str(project_path), "--defaults"]
  for key, value in params.items():
    if value is not None:
      command.extend(["--data", f"{key}={value}"])

  result = run_command(str(PROJECT_ROOT), shlex.join(command))

  if result.error is None:
    if saved_node_modules is not None:
      saved_node_modules.rename(node_modules)
      saved_node_modules.parent.rmdir()

    answers_path = project_path / ".copier-answers.yml"
    answers = answers_path.read_text()
    answers = re.sub(r'^_commit:.*$', '_commit: "0000000"', answers, count=1, flags=re.MULTILINE)
    answers_path.write_text(answers.rstrip() + "\n")

  return result
