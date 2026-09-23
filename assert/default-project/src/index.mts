import * as core from '@actions/core';

import {run} from './action/run.mts';

try {
  await run();
} catch (error) {
  core.setFailed(error instanceof Error ? error.message : `Action failed with unexpected error: ${String(error)}`);
}
