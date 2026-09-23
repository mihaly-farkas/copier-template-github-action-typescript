import {test, expect, vi} from 'vitest';
import * as core from '@actions/core';

vi.mock('@actions/core', () => ({
  setFailed: vi.fn(),
}));

async function importAction(): Promise<void> {
  vi.resetModules();
  await import('./index.mts');
}

async function importRun(): Promise<() => Promise<boolean>> {
  vi.resetModules();
  const action = await import('./index.mts');
  return action.run;
}

beforeEach(() => {
  vi.clearAllMocks();
});

test('my-action GitHub Action fails (not implemented yet)', async () => {
  // ACT
  await importAction();

  // ASSERT
  expect(core.setFailed).toHaveBeenCalledTimes(1);
  expect(core.setFailed).toHaveBeenCalledWith('my-action GitHub Action is not implemented yet!');
});

test('my-action GitHub Action reports an unsuccessful run', async () => {
  // ACT
  const run = await importRun();
  const success = await run();

  // ASSERT
  expect(success).toBe(false);
});
