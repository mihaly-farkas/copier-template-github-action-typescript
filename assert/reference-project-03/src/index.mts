import * as core from '@actions/core';

import customAction03 from './action/custom-action-03.mts';

try {
  await customAction03(core);
} catch (error) {
  core.setFailed(error instanceof Error ? error.message : `Action failed with unexpected error: ${String(error)}`);
}
