import subprocess

from langchain_core.tools import tool


@tool
def execute_bash_command(command: str) -> str:
  """Executes a bash command in the project workspace and returns the stdout/stderr.
  Use this to inspect files (e.g., cat, diff), modify content, copy files, or run scripts.
  Always use non-interactive commands.
  """
  try:
    result = subprocess.run(
      command,
      shell=True,
      capture_output=True,
      text=True,
      timeout=30
    )

    output = []
    if result.stdout:
      output.append(result.stdout)
    if result.stderr:
      output.append(f"STDERR:\n{result.stderr}")

    if not output:
      return f"Command executed successfully with exit code {result.returncode} (No output)."

    return "\n".join(output)
  except subprocess.TimeoutExpired:
    return "Error: Command timed out after 30 seconds."
  except Exception as e:
    return f"Error executing command: {str(e)}"
