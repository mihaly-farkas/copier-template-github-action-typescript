import {beforeEach, expect, test, vi} from 'vitest';

import * as core from '@actions/core';
import dynamicToken1fe1a5f3 from './dynamic-token-1fe1a5f3.mts';

vi.mock('@actions/core', () => ({
  setFailed: vi.fn(),
}));

beforeEach(() => {
  vi.clearAllMocks();
});

test('DYNAMIC_TOKEN:1fe1a5f3 fails (not implemented yet)', async () => {
  // ACT
  await dynamicToken1fe1a5f3(core);
  // ASSERT
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('DYNAMIC_TOKEN:1fe1a5f3 is not implemented yet!');
});
