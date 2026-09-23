/**
 * @file spec/copy-default.spec.mts
 * @description Tests for the project generated with the default parameters.
 *
 * This test suite verifies that the project generated with the default parameters can be generated, dependencies can
 * be installed, tests can be run, and the generated project matches the reference project.
 *
 * The execution order of the test is important. The tests are designed to be run in the order they are defined, the
 * tests are **NOT INDEPENDENT**.
 *
 * In practice, it works with three different directories:
 * 1. The `<project_root>/template/` directory contains the **Template Blueprint** files that are used to generate the
 *    project.
 * 2. The `<project_root>/assert/default-project/` directory contains the **Reference Project** that is used to compare
 *    the generated project.
 * 3. During the test execution, a temporary directory is created in the `<project_root>/.tmp/default-project/`
 *    directory, where the project is generated from the **Template Blueprint** and tested against the
 *    **Reference Project**.
 *
 * The test suite uses Vitest as the testing framework and is designed to be run in a Node.js environment.
 * The tests are written in TypeScript and use the ES module syntax.
 */
import {test} from 'vitest';
import {getDefaultTemplateParameters} from './lib/get-default-template-parameters.mts';
import {generateProject} from './lib/generate-project.mts';
import {getProjectDirName} from './lib/get-project-dir-name.mts';
import {getAssertDirName} from './lib/get-assert-dir-name.mts';
import {compareFiles} from './lib/compare-files.mts';
import {runCommand} from './lib/run-command.mts';

const defaultCase = 'default-project';
const ignoreList = ['.idea/.*', 'build/.*', 'coverage/.*', 'node_modules/.*', '.*\\.iml', 'package-lock\\.json'];

test('A project can be generated with the default parameters', async () => {
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

test('A project generated with the default parameters can install npm dependencies', async () => {
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

test('A project generated with the default parameters can run generated tests without error', async () => {
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

test('A project generated with the default parameters matches the reference project', async () => {
  // ARRANGE
  const projectDir = getProjectDirName(defaultCase);
  const referenceProjectDir = getAssertDirName(defaultCase);

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
