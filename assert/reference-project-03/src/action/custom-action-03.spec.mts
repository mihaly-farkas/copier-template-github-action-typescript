import {beforeEach, expect, test, vi} from 'vitest';

import * as core from '@actions/core';
import customAction03 from './custom-action-03.mts';

vi.mock('@actions/core', () => ({
  setFailed: vi.fn(),
}));

beforeEach(() => {
  vi.clearAllMocks();
});

test('Custom Action 03 fails (not implemented yet)', async () => {
  // ACT
  await customAction03(core);
  // ASSERT
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('Custom Action 03 is not implemented yet!');
});
