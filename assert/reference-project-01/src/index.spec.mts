import {beforeEach, expect, test, vi} from 'vitest';

import * as core from '@actions/core';
import dynamicToken1fe1a5f3 from './action/dynamic-token-1fe1a5f3.mts';

vi.mock('./action/dynamic-token-1fe1a5f3.mts', () => ({
  default: vi.fn(),
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
  expect(dynamicToken1fe1a5f3).toHaveBeenCalledTimes(1);
});

test('index.mts marks the action as failed when the implementation throws', async () => {
  // ARRANGE
  vi.mocked(dynamicToken1fe1a5f3).mockRejectedValueOnce(new Error('Example failure'));
  // ACT
  await import('./index.mts');
  // ASSERT
  expect(dynamicToken1fe1a5f3).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('Example failure');
});

test('index.mts marks the action as failed when the implementation throws a string', async () => {
  // ARRANGE
  vi.mocked(dynamicToken1fe1a5f3).mockRejectedValueOnce('Example string failure');
  // ACT
  await import('./index.mts');
  // ASSERT
  expect(dynamicToken1fe1a5f3).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('Action failed with unexpected error: Example string failure');
});
