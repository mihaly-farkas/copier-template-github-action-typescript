import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CommandResult:
  cwd: str
  command: str
  stdout: str = ""
  stderr: str = ""
  error: Optional[Exception] = None


def run_command(cwd: Optional[str], command: str) -> CommandResult:
  result = subprocess.run(
    command,
    cwd=cwd,
    shell=True,
    capture_output=True,
    text=True,
    check=False,
  )
  error = (
    None
    if result.returncode == 0
    else RuntimeError(f"Command failed with exit code {result.returncode}")
  )
  return CommandResult(
    cwd=cwd or ".",
    command=command,
    stdout=result.stdout.strip(),
    stderr=result.stderr.strip(),
    error=error,
  )
