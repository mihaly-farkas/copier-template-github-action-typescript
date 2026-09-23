import {defineConfig} from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    include: ['**/*.spec.mts'],
    exclude: ['**/.local/**', '**/node_modules/**', '**/build/**', '**/dist/**'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.mts'],
      exclude: ['src/**/*.spec.mts'],
      thresholds: {
        lines: 100,
        functions: 100,
        branches: 100,
        statements: 100,
        perFile: true,
      },
    },
  },
});
