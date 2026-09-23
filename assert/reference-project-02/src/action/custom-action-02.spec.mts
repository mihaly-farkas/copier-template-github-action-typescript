import {beforeEach, expect, test, vi} from 'vitest';

import * as core from '@actions/core';
import customAction02 from './custom-action-02.mts';

vi.mock('@actions/core', () => ({
  setFailed: vi.fn(),
}));

beforeEach(() => {
  vi.clearAllMocks();
});

test('Custom Action 02 fails (not implemented yet)', async () => {
  // ACT
  await customAction02(core);
  // ASSERT
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('Custom Action 02 is not implemented yet!');
});
