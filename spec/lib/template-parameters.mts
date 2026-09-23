export interface TemplateParameters extends Record<string, string | number | undefined> {
  licenseOwner: string;
  licenseYearStart?: number;
  githubRepositoryOwner: string;
  githubRepositoryName: string;
  githubActionName: string;
  githubActionDescription: string;
  githubActionExampleStepName: string;
}
