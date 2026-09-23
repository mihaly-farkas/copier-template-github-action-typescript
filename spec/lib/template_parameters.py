from typing import TypedDict


class TemplateParameters(TypedDict, total=False):
  licenseOwner: str
  licenseYearStart: int
  githubRepositoryOwner: str
  githubRepositoryName: str
  githubActionName: str
  githubActionDescription: str
  githubActionExampleStepName: str


def get_default_template_parameters() -> TemplateParameters:
  return {
    "licenseOwner": "My Name",
    "githubRepositoryOwner": "my-github-username",
    "githubRepositoryName": "my-repo",
    "githubActionName": "my-action",
    "githubActionDescription": "My GitHub Action",
    "githubActionExampleStepName": "My Example Step",
  }
