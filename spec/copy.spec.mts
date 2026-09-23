import {test} from 'vitest';
import {getDefaultTemplateParameters} from './lib/get-default-template-parameters.mts';
import {generateProject} from './lib/generate-project.mts';
import {getProjectDirName} from './lib/get-project-dir-name.mts';
import {getAssetDirName} from './lib/get-asset-dir-name.mts';
import {compareFiles} from './lib/compare-files.mts';
import {runCommand} from './lib/run-command.mts';

const defaultCase = 'default-project';
const ignoreList = ['.idea/.*', 'build/.*', 'node_modules/.*', '.*\\.iml', 'package-lock\\.json'];

test('Project generated with the default parameters without error', async () => {
  // ARRANGE
  const projectDir = getProjectDirName(defaultCase);
  const params = getDefaultTemplateParameters();

  // ACT
  const result = generateProject(projectDir, params);

  // ASSERT
  const message = () =>
    'Execution failed. ' +
    JSON.stringify({
      commandExecutionResult: result,
    });
  expect(result.error, message()).toBeUndefined();
});

test('Project generated with the default parameters installs dependencies without error', async () => {
  // ARRANGE
  const projectDir = getProjectDirName(defaultCase);

  // ACT
  const result = runCommand(projectDir, 'npm install');

  // ASSERT
  const message = () =>
    'Execution failed. ' +
    JSON.stringify({
      commandExecutionResult: result,
    });
  expect(result.error, message()).toBeUndefined();
}, 60000);

test('Project generated with the default parameters runs tests without error', async () => {
  // ARRANGE
  const projectDir = getProjectDirName(defaultCase);

  // ACT
  const result = runCommand(projectDir, 'npm run test');

  // ASSERT
  const message = () =>
    'Execution failed. ' +
    JSON.stringify({
      commandExecutionResult: result,
    });
  expect(result.error, message()).toBeUndefined();
}, 60000);

test('Project generated with the default parameters matches the reference project', async () => {
  // ARRANGE
  const projectDir = getProjectDirName(defaultCase);
  const referenceProjectDir = getAssetDirName(defaultCase);

  // ACT & ASSERT
  compareFiles(projectDir, referenceProjectDir, {
    ignoreList,
    compareCallback: (actualFile, referenceFile) => {
      const message = () =>
        'File contents do not match. ' +
        JSON.stringify({
          actualFile: actualFile.path,
          referenceFile: referenceFile.path,
        });
      expect(actualFile.content, message()).toEqual(referenceFile.content);
    },
    nonExpectedFileCallback: nonExpectedFile => {
      const message = () =>
        'Non-expected file found. ' +
        JSON.stringify({
          nonExpectedFilePath: nonExpectedFile.path,
        });
      expect(nonExpectedFile, message()).toBeUndefined();
    },
  });
});
