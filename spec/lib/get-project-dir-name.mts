export function getProjectDirName(relativePath: string): string {
  return `${import.meta.dirname}/../../.tmp/${relativePath}`;
}
