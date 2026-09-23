import {execSync} from 'node:child_process';
import {existsSync, mkdirSync, mkdtempSync, renameSync, rmSync} from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import {CommandResult, runCommand} from './run-command.mts';

export function generateProject(
  projectDir: string,
  params: Record<string, string | number | undefined>,
): CommandResult {
  // Normalize the project directory path
  projectDir = path.resolve(projectDir);

  // Create the parent directory of the project directory if it doesn't exist
  const parentDir = path.dirname(projectDir);
  mkdirSync(parentDir, {recursive: true});

  // If the project directory already exists, and there is a node_modules directory, save it to a tmp directory
  // for restoration, to avoid re-downloading dependencies
  let tmpDir: string | undefined;
  if (existsSync(projectDir) && existsSync(path.join(projectDir, 'node_modules'))) {
    tmpDir = mkdtempSync(path.join(os.tmpdir(), 'copier-'));
    renameSync(path.join(projectDir, 'node_modules'), path.join(tmpDir, 'node_modules'));
  }

  // Remove the project directory if it already exists
  rmSync(projectDir, {recursive: true, force: true});

  // Construct the Copier command
  let command = `copier copy . ${projectDir} --defaults`;

  // Append parameters to the command
  for (const [key, value] of Object.entries(params)) {
    command += ` --data ${key}="${value}"`;
  }

  // Execute the command
  const executionResult = runCommand('.', command);

  if (executionResult.error) {
    return executionResult;
  }

  // If there is a tmp directory with node_modules, restore it
  if (tmpDir) {
    renameSync(path.join(tmpDir, 'node_modules'), path.join(projectDir, 'node_modules'));
  }

  // Rewrite _commit value in .copier-answers.yml to a fixed value to avoid test failures due to different commits
  const answersFilePath = path.join(projectDir, '.copier-answers.yml');
  execSync(`yq eval '.["_commit"] = "0000000"' -i "${answersFilePath}"`, {stdio: 'inherit'});

  return executionResult;
}
