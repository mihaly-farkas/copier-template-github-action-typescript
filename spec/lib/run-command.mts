import {execSync} from 'node:child_process';

export interface CommandResult {
  readonly cwd: string;
  readonly command: string;
  readonly output: string;
  readonly error?: Error;
}

export const runCommand = (cwd: string, command: string): CommandResult => {
  try {
    const output = execSync(command, {cwd, encoding: 'utf8'});
    return {cwd, command, output};
  } catch (error) {
    const commandError = error instanceof Error ? error : new Error(String(error));
    const output = error instanceof Error && 'stdout' in error && typeof error.stdout === 'string' ? error.stdout : '';
    return {cwd, command, output, error: commandError};
  }
};
