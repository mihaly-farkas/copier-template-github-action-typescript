import {TemplateParameters} from './template-parameters.mts';

export function getDefaultTemplateParameters(): TemplateParameters {
  return {
    licenseOwner: 'My Name',
    githubRepositoryOwner: 'my-github-username',
    githubRepositoryName: 'my-repo',
    githubActionName: 'my-action',
    githubActionDescription: 'My GitHub Action',
    githubActionExampleStepName: 'My Example Step',
  };
}
