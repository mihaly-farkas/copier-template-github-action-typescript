import {spawnSync} from 'node:child_process';

export interface CommandResult {
  readonly cwd: string;
  readonly command: string;
  readonly stdout?: string;
  readonly stderr?: string;
  readonly error?: Error;
}

export const runCommand = (cwd: string, command: string): CommandResult => {
  const result = spawnSync(command, {cwd, encoding: 'utf8', shell: true});

  const stdout = result.stdout ? result.stdout.trim() : '';
  const stderr = result.stderr ? result.stderr.trim() : '';

  let error: Error | undefined = undefined;
  if (result.error) {
    error = result.error;
  } else if (result.status !== 0) {
    error = new Error(`Command failed with exit code ${result.status}`);
  }

  return {
    cwd,
    command,
    stdout,
    stderr,
    error,
  };
};
