import * as core from '@actions/core';

export const run = async (): Promise<boolean> => {
  core.setFailed('my-action GitHub Action is not implemented yet!');
  return false;
};

try {
  await run();
} catch (error) {
  core.setFailed(`Action failed with error: ${error}`);
}
