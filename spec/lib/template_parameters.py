from typing import TypedDict


class TemplateParameters(TypedDict, total=False):
  licenseOwner: str
  licenseYearStart: int
  githubRepositoryOwner: str
  githubRepositoryName: str
  githubActionName: str
  githubActionNameCamelCase: str
  githubActionNameKebabCase: str
  githubActionDescription: str
  githubActionExampleStepName: str
