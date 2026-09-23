import gts from 'gts';
import globals from 'globals';
import type {Linter} from 'eslint';

let customConfig: Linter.Config[] = [];
let hasIgnoresFile = false;

const withModuleTsExtensions = (config: Linter.Config): Linter.Config => {
  if (!config.files) {
    return config;
  }

  return {
    ...config,
    files: config.files.flatMap((filePattern: string | string[]) =>
      (Array.isArray(filePattern) ? filePattern : [filePattern]).flatMap(pattern => {
        if (pattern === '**/*.ts') {
          return ['**/*.ts', '**/*.mts'];
        }

        if (pattern === '**/*.tsx') {
          return ['**/*.tsx', '**/*.mtsx'];
        }

        return [pattern];
      }),
    ),
  };
};

const gtsWithModuleTsExtensions = gts.map(withModuleTsExtensions);

try {
  // noinspection JSFileReferences
  await import('./eslint.ignores.mts');
  hasIgnoresFile = true;
} catch {
  // eslint.ignores.js doesn't exist
}

if (hasIgnoresFile) {
  // noinspection JSFileReferences
  const {default: ignores} = await import('./eslint.ignores.mts');
  customConfig = [{ignores}];
}

export default [
  ...customConfig,
  ...gtsWithModuleTsExtensions,
  {
    rules: {
      'max-len': [
        'error',
        {
          code: 120,
        },
      ],
    },
  },
  {
    files: ['**/*.spec.mts', '**/*.spec.ts'],
    languageOptions: {
      globals: globals.jest,
    },
    rules: {
      'max-len': [
        'error',
        {
          code: 120,
          ignoreStrings: true,
          ignoreTemplateLiterals: true,
        },
      ],
    },
  },
];
