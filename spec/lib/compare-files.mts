import {visitFiles} from './visit-files.mts';
import {existsSync, readFileSync} from 'node:fs';
import path from 'node:path';

export interface CompareFilesOptions {
  ignoreList?: string[];
  compareCallback?: (
    actualFile: {path: string; content: string},
    referenceFile: {
      path: string;
      content: string;
    },
  ) => void;
  nonExpectedFileCallback?: (nonExpectedFile: {path: string; content: string}) => void;
}

export function compareFiles(actualDir: string, expectedDir: string, options: CompareFilesOptions = {}) {
  const {ignoreList = [], compareCallback, nonExpectedFileCallback} = options;

  if (compareCallback) {
    visitFiles(expectedDir, ignoreList, filename => {
      const generatedFilePath = path.resolve(actualDir, filename);
      const referenceFilePath = path.resolve(expectedDir, filename);

      // Read the contents of the generated file and the reference file
      const generatedFileContent = readFileSync(generatedFilePath, 'utf-8');
      const referenceFileContent = readFileSync(referenceFilePath, 'utf-8');

      compareCallback(
        {path: generatedFilePath, content: generatedFileContent},
        {
          path: referenceFilePath,
          content: referenceFileContent,
        },
      );
    });
  }

  if (nonExpectedFileCallback) {
    visitFiles(actualDir, ignoreList, filename => {
      const referenceFilePath = path.resolve(expectedDir, filename);

      // Check if the file exists in the reference project
      const referenceFileExists = existsSync(referenceFilePath);
      if (!referenceFileExists) {
        nonExpectedFileCallback({path: referenceFilePath, content: readFileSync(referenceFilePath, 'utf-8')});
      }
    });
  }
}
