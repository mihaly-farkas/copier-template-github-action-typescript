import path from 'node:path';

export function getAssertDirName(relativePath: string): string {
  return path.resolve(`${import.meta.dirname}/../../assert/${relativePath}`);
}
