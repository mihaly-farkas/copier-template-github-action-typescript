import {beforeEach, expect, test, vi} from 'vitest';

import * as core from '@actions/core';
import {run} from './run.mts';

vi.mock('@actions/core', () => ({
  setFailed: vi.fn(),
}));

beforeEach(() => {
  vi.clearAllMocks();
});

test('my-action GitHub Action fails (not implemented yet)', async () => {
  // ACT
  await run();

  // ASSERT
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('my-action GitHub Action is not implemented yet!');
});
