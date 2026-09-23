/**
 * @file spec/copy-license-year-start.spec.mts
 * @description Tests that the configured license start year is included in the generated LICENSE file.
 */
import {readFileSync} from 'node:fs';
import * as path from 'node:path';
import {test} from 'vitest';
import {generateProject} from './lib/generate-project.mts';
import {getDefaultTemplateParameters} from './lib/get-default-template-parameters.mts';
import {getProjectDirName} from './lib/get-project-dir-name.mts';

test.each([2022, 2023, 2024])(
  'A generated LICENSE file includes the configured license start year when the licenseYearStart parameter is %s',
  async licenseYearStart => {
    // ARRANGE
    const projectDir = getProjectDirName(`license-year-start-project-${licenseYearStart}`);
    const licenseFilePath = path.join(projectDir, 'LICENSE');
    const params = {
      ...getDefaultTemplateParameters(),
      licenseYearStart,
    };

    // ACT
    const result = generateProject(projectDir, params);

    // ASSERT
    const message = () =>
      'Execution failed. ' +
      JSON.stringify({
        commandExecutionResult: result,
      });
    expect(result.error, message()).toBeUndefined();

    const licenseContent = readFileSync(licenseFilePath, 'utf8');
    expect(licenseContent).toContain(`Copyright (c) ${licenseYearStart}-2026 My Name`);
  },
);
