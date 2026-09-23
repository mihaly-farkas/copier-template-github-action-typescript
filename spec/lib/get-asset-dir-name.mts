import path from 'node:path';

export function getAssetDirName(relativePath: string): string {
  return path.resolve(`${import.meta.dirname}/../../asset/${relativePath}`);
}
