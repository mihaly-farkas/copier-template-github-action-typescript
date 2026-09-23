import * as core from '@actions/core';

import dynamicToken1fe1a5f3 from './action/dynamic-token-1fe1a5f3.mts';

try {
  await dynamicToken1fe1a5f3(core);
} catch (error) {
  core.setFailed(error instanceof Error ? error.message : `Action failed with unexpected error: ${String(error)}`);
}
