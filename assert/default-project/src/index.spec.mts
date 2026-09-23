import {beforeEach, expect, test, vi} from 'vitest';

import * as core from '@actions/core';
import {run} from './action/run.mts';

vi.mock('./action/run.mts', () => ({
  run: vi.fn(),
}));

vi.mock('@actions/core', () => ({
  setFailed: vi.fn(),
}));

beforeEach(() => {
  vi.clearAllMocks();
  vi.resetModules();
});

test('index.mts runs the action implementation once', async () => {
  // ACT
  await import('./index.mts');

  // ASSERT
  expect(run).toHaveBeenCalledTimes(1);
});

test('index.mts marks the action as failed when the implementation throws', async () => {
  // ARRANGE
  vi.mocked(run).mockRejectedValueOnce(new Error('Example failure'));

  // ACT
  await import('./index.mts');

  // ASSERT
  expect(run).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('Example failure');
});

test('index.mts marks the action as failed when the implementation throws a string', async () => {
  // ARRANGE
  vi.mocked(run).mockRejectedValueOnce('Example string failure');

  // ACT
  await import('./index.mts');

  // ASSERT
  expect(run).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('Action failed with unexpected error: Example string failure');
});
