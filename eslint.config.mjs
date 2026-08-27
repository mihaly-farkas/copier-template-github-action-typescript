import chaiFriendly from 'eslint-plugin-chai-friendly';
import gts from 'gts';

let customConfig = [];
let hasIgnoresFile = false;

try {
  await import('./eslint.ignores.mjs');
  hasIgnoresFile = true;
} catch {
  // eslint.ignores.js doesn't exist
}

if (hasIgnoresFile) {
  const {default: ignores} = await import('./eslint.ignores.mjs');
  customConfig = [{ignores}];
}

export default [
  ...customConfig,
  ...gts,
  {
    plugins: {
      'chai-friendly': chaiFriendly,
    },

    rules: {
      'max-len': [
        'error',
        {
          code: 120,
        },
      ],
      '@typescript-eslint/no-unused-expressions': 'off',
      'chai-friendly/no-unused-expressions': 'error',
    },
  },
];
