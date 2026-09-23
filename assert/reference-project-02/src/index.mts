import * as core from '@actions/core';

import customAction02 from './action/custom-action-02.mts';

try {
  await customAction02(core);
} catch (error) {
  core.setFailed(error instanceof Error ? error.message : `Action failed with unexpected error: ${String(error)}`);
}
