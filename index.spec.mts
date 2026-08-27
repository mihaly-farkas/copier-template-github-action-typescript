import { test, expect, vi } from 'vitest';
import * as core from '@actions/core';

vi.mock('@actions/core', () => ({
  setFailed: vi.fn(),
}));

test('a script meghívja a setFailed-et a megfelelő hibaüzenettel', async () => {
  // ACT
  await import('./index.mts');

  // ASSERT
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith(
    'Maven Prepare GitHub Action is not implemented!'
  );
});
