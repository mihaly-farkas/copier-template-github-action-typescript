import fs from 'node:fs';
import path from 'node:path';

export const visitFiles = (baseDir: string, ignorePatterns: string[], callback: (relativeFilename: string) => void) => {
  baseDir = path.resolve(baseDir);

  const visitDir = (currentDir: string) => {
    for (const entry of fs.readdirSync(currentDir, {withFileTypes: true})) {
      const entryPath = path.join(currentDir, entry.name);

      if (entry.isDirectory()) {
        visitDir(entryPath);
      } else if (entry.isFile()) {
        const relativeFilename = path.relative(baseDir, entryPath).split(path.sep).join('/');
        if (!ignorePatterns.some(pattern => new RegExp(pattern).test(relativeFilename))) {
          callback(relativeFilename);
        }
      }
    }
  };

  visitDir(baseDir);
};
