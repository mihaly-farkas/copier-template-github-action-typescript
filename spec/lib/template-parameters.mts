export interface TemplateParameters extends Record<string, string | number | undefined> {
  readonly licenseOwner: string;
  readonly licenseYearStart?: number;
  readonly githubRepositoryOwner: string;
  readonly githubRepositoryName: string;
  readonly githubActionName: string;
  readonly githubActionDescription: string;
  readonly githubActionExampleStepName: string;
}
