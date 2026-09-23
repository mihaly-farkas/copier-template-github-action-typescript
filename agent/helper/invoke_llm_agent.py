from datetime import datetime as _datetime
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_githubcopilot_chat import ChatGithubCopilot
from pathlib import Path
from rich import print
from typing import Any
from typing import Any, TypedDict, Optional, List, Union

from agent.helper.print_separator import print_separator

GITHUB_COPILOT = "github-copilot"


class InvokeLlmAgentProps(TypedDict):
  prompt: str
  model: str
  temperature: float
  skill: Optional[str]
  tools: List = []


class LlmAgentInvocationMetadata:
  type: str
  model: str
  temperature: float
  skill_path: Optional[str]
  skill_content: Optional[str]

  def __init__(
    self,
    type: str,
    model: str,
    temperature: float,
    skill_path: Optional[str],
    skill_content: Optional[str],
  ):
    self.type = type
    self.model = model
    self.temperature = temperature
    self.skill_path = skill_path
    self.skill_content = skill_content


class LlmAgentInvocationResponse:
  messages: List[Union[HumanMessage, AIMessage, ToolMessage]]

  def __init__(self, messages: List[Union[HumanMessage, AIMessage, ToolMessage]]):
    self.messages = messages


class LlmAgentInvocation:
  event: str
  datetime: _datetime
  node: str
  metadata: LlmAgentInvocationMetadata
  response: LlmAgentInvocationResponse

  def __init__(
    self,
    node: str,
    metadata: LlmAgentInvocationMetadata,
    response: LlmAgentInvocationResponse
  ):
    self.event = "llm_agent_invocation"
    self.datetime = _datetime.now()
    self.node = node
    self.metadata = metadata
    self.response = response


def invoke_llm_agent(props: InvokeLlmAgentProps) -> LlmAgentInvocation:
  node = props.get("node")
  model = props["model"]
  prompt = props["prompt"]
  type = props.get("type", GITHUB_COPILOT)
  temperature = props.get("temperature", 0.2)
  skill_path_str = props.get("skill")
  tools = props.get("tools")

  print_separator("Invoke LLM agent")
  print(f"[dim]Node:        {node}[/dim]")
  print(f"[dim]Type:        {type}[/dim]")
  print(f"[dim]Model:       {model}[/dim]")
  print(f"[dim]Temperature: {temperature}[/dim]")

  system_prompt = None

  skill = None
  if skill_path_str is not None:
    skill_path = Path(skill_path_str)
    print(f"[dim]Skill path:  {skill_path}[/dim]")

    # print_separator("SKILL.md")
    if not skill_path.exists():
      raise FileNotFoundError(f"SKILL.md not found at {skill_path}")
    skill = skill_path.read_text(encoding="utf-8")
    # print(f"[dim]{skill}[/dim]")
    system_prompt = skill

  print_separator("Prompt")
  print(f"[dim]{prompt}[/dim]")

  llm = None

  if type == GITHUB_COPILOT:
    llm = ChatGithubCopilot(
      model=model,
      temperature=temperature
    )
  else:
    raise ValueError(f"Unsupported LLM type: {model}")

  agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
  )

  response = agent.invoke({"messages": [("user", prompt)]})

  return LlmAgentInvocation(
    node=node,
    metadata=LlmAgentInvocationMetadata(
      type=type,
      model=model,
      temperature=temperature,
      skill_path=skill_path_str,
      skill_content=skill,
    ),
    response=LlmAgentInvocationResponse(
      messages=response["messages"]
    )
  )
