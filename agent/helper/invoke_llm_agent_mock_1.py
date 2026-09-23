from datetime import datetime as _datetime
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_githubcopilot_chat import ChatGithubCopilot
from pathlib import Path
from rich import print
from typing import Any

from agent.helper.invoke_llm_agent import InvokeLlmAgentProps, LlmAgentInvocation, GITHUB_COPILOT, \
  LlmAgentInvocationMetadata, \
  LlmAgentInvocationResponse
from agent.helper.print_separator import print_separator


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

  response = {
    "messages": [
      HumanMessage(
        content="Modify the _Template Blueprint_ to implement the changes in the _Reference Template_.\n\nThe following files should be added in the _Reference Template_:\n- `DUMMY`\n\nThe following files should be modified in the\n_Reference Template_:\n- `tsconfig.json`\n\n",
        additional_kwargs={},
        response_metadata={},
        id="cb64a75a-ffed-4266-bc1a-63949fb7ae9f",
      ),
      AIMessage(
        content="",
        additional_kwargs={"refusal": None},
        response_metadata={
          "token_usage": {
            "completion_tokens": 81,
            "prompt_tokens": 501,
            "total_tokens": 582,
            "completion_tokens_details": {
              "accepted_prediction_tokens": 0,
              "audio_tokens": None,
              "reasoning_tokens": None,
              "rejected_prediction_tokens": 0,
              "text_tokens": None,
            },
            "prompt_tokens_details": {
              "audio_tokens": None,
              "cache_write_tokens": None,
              "cached_tokens": 0,
              "image_tokens": None,
              "text_tokens": None,
            },
          },
          "model_provider": "openai",
          "model_name": "gpt-4o-2024-11-20",
          "system_fingerprint": "fp_2b2e565915",
          "id": "chatcmpl-ERby4I8Uj73G390kleMrPfeA8YfMj",
          "service_tier": "default",
          "finish_reason": "tool_calls",
          "logprobs": None,
        },
        id="lc_run--01a0d32f-ab95-7643-9521-7178ce65b42f-0",
        tool_calls=[
          {
            "name": "execute_bash_command",
            "args": {"command": "cat assert/reference-project-01/DUMMY"},
            "id": "call_q2XB8TZXMdRavjw3WXgMLDPq",
            "type": "tool_call",
          },
          {
            "name": "execute_bash_command",
            "args": {"command": "cat assert/reference-project-01/tsconfig.json"},
            "id": "call_8mTylTpaRE3jv4RQs9KSyBpD",
            "type": "tool_call",
          },
          {
            "name": "execute_bash_command",
            "args": {"command": "ls template"},
            "id": "call_WjblPs8nxoxgZ2Ts354xh6nq",
            "type": "tool_call",
          },
        ],
      ),
      ToolMessage(
        content="DUMMY\n",
        name="execute_bash_command",
        id="ba5f5194-1abe-4aa2-87c4-3c6c1701014d",
        tool_call_id="call_q2XB8TZXMdRavjw3WXgMLDPq",
      ),
      ToolMessage(
        content='{\n  "extends": "./node_modules/gts/tsconfig-google.json",\n  "compilerOptions": {\n    "rootDir": ".",\n    "outDir": "build",\n    "module": "NodeNext",\n    "moduleResolution": "NodeNext",\n"allowImportingTsExtensions": true,\n    "lib": [\n      "ES2024",\n      "DOM",\n      "DOM.Iterable"\n    ],\n    "noEmit": true,\n    "types": [\n      "node",\n      "vitest/globals"\n    ]\n  },\n  "include": [\n"src/**/*.mts",\n    "*.mts",\n    ".prettierrc.mts",\n  ],\n  "exclude": [\n    ".local",\n    "node_modules",\n    "build"\n  ]\n}\n',
        name="execute_bash_command",
        id="ddc56307-3cf0-4e91-a79a-307f4de16c98",
        tool_call_id="call_8mTylTpaRE3jv4RQs9KSyBpD",
      ),
      ToolMessage(
        content="README.md.j2\naction.yml.j2\neslint.config.mts\neslint.ignores.mts\npackage.json.j2\nsrc\ntemplate.iml\ntool\ntsconfig.json\nvitest.config.mts\n{{ 'LICENSE' }}.j2\n{{ _copier_conf.answers_file }}.j2\n",
        name="execute_bash_command",
        id="73911a18-2c26-4a32-8282-534e92c23abe",
        tool_call_id="call_WjblPs8nxoxgZ2Ts354xh6nq",
      ),
      AIMessage(
        content="",
        additional_kwargs={"refusal": None},
        response_metadata={
          "token_usage": {
            "completion_tokens": 30,
            "prompt_tokens": 875,
            "total_tokens": 905,
            "completion_tokens_details": {
              "accepted_prediction_tokens": 0,
              "audio_tokens": None,
              "reasoning_tokens": None,
              "rejected_prediction_tokens": 0,
              "text_tokens": None,
            },
            "prompt_tokens_details": {
              "audio_tokens": None,
              "cache_write_tokens": None,
              "cached_tokens": 0,
              "image_tokens": None,
              "text_tokens": None,
            },
          },
          "model_provider": "openai",
          "model_name": "gpt-4o-2024-11-20",
          "system_fingerprint": "fp_2b2e565915",
          "id": "chatcmpl-ERby73QGcxXH6gdzrRVtjqAa0x4Hg",
          "service_tier": "default",
          "finish_reason": "tool_calls",
          "logprobs": None,
        },
        id="lc_run--01a0d32f-b8ef-7cc2-afad-8f5203f7dedf-0",
        tool_calls=[
          {
            "name": "execute_bash_command",
            "args": {
              "command": "diff template/tsconfig.json assert/reference-project-01/tsconfig.json"
            },
            "id": "call_VZEkgoBrF7h8XQ9rTyYQ1TbN",
            "type": "tool_call",
          }
        ],
      ),
      ToolMessage(
        content='24d23\n<     "vitest.config.mts"\n',
        name="execute_bash_command",
        id="6fc46ff3-96d0-4d1a-b139-3fc4fdc28a93",
        tool_call_id="call_VZEkgoBrF7h8XQ9rTyYQ1TbN",
      ),
      AIMessage(
        content="",
        additional_kwargs={"refusal": None},
        response_metadata={
          "token_usage": {
            "completion_tokens": 74,
            "prompt_tokens": 928,
            "total_tokens": 1002,
            "completion_tokens_details": {
              "accepted_prediction_tokens": 0,
              "audio_tokens": None,
              "reasoning_tokens": None,
              "rejected_prediction_tokens": 0,
              "text_tokens": None,
            },
            "prompt_tokens_details": {
              "audio_tokens": None,
              "cache_write_tokens": None,
              "cached_tokens": 0,
              "image_tokens": None,
              "text_tokens": None,
            },
          },
          "model_provider": "openai",
          "model_name": "gpt-4o-2024-11-20",
          "system_fingerprint": "fp_2b2e565915",
          "id": "chatcmpl-ERby9gFa2Lf3Fx7370Aho6U82LQ5I",
          "service_tier": "default",
          "finish_reason": "tool_calls",
          "logprobs": None,
        },
        id="lc_run--01a0d32f-c21a-77b3-b808-d17e0e694281-0",
        tool_calls=[
          {
            "name": "execute_bash_command",
            "args": {"command": "echo 'DUMMY' > template/DUMMY"},
            "id": "call_lQXgqvRRWskelpSNowysUbNo",
            "type": "tool_call",
          },
          {
            "name": "execute_bash_command",
            "args": {
              "command": "sed -i '/\"vitest.config.mts\"/d' template/tsconfig.json"
            },
            "id": "call_fmOvBJntdHhdaXdjSL8ywXlN",
            "type": "tool_call",
          },
        ],
      ),
      ToolMessage(
        content="Command executed successfully with exit code 0 (No output).",
        name="execute_bash_command",
        id="26d587b3-9f99-40bf-8dbc-b22c2ce8ef02",
        tool_call_id="call_lQXgqvRRWskelpSNowysUbNo",
      ),
      ToolMessage(
        content='STDERR:\nsed: 2: "template/tsconfig.json\n": undefined label \'emplate/tsconfig.json\'\n',
        name="execute_bash_command",
        id="a4cb4417-ea3f-4acc-a8d6-6a64c77f53a8",
        tool_call_id="call_fmOvBJntdHhdaXdjSL8ywXlN",
      ),
      AIMessage(
        content="",
        additional_kwargs={"refusal": None},
        response_metadata={
          "token_usage": {
            "completion_tokens": 35,
            "prompt_tokens": 1055,
            "total_tokens": 1090,
            "completion_tokens_details": {
              "accepted_prediction_tokens": 0,
              "audio_tokens": None,
              "reasoning_tokens": None,
              "rejected_prediction_tokens": 0,
              "text_tokens": None,
            },
            "prompt_tokens_details": {
              "audio_tokens": None,
              "cache_write_tokens": None,
              "cached_tokens": 0,
              "image_tokens": None,
              "text_tokens": None,
            },
          },
          "model_provider": "openai",
          "model_name": "gpt-4o-2024-11-20",
          "system_fingerprint": "fp_2b2e565915",
          "id": "chatcmpl-ERbyBaDdn1UMkuZWrURvNsSfRvwHp",
          "service_tier": "default",
          "finish_reason": "tool_calls",
          "logprobs": None,
        },
        id="lc_run--01a0d32f-c884-7701-bc01-4fd0f29bb3ec-0",
        tool_calls=[
          {
            "name": "execute_bash_command",
            "args": {
              "command": "sed -i '' '/\"vitest.config.mts\"/d' template/tsconfig.json"
            },
            "id": "call_9ugEC0r5R0VPT2lYXt00Jyej",
            "type": "tool_call",
          }
        ],
      ),
      ToolMessage(
        content="Command executed successfully with exit code 0 (No output).",
        name="execute_bash_command",
        id="8c660f89-fb2d-40d1-83e5-f6b644341d39",
        tool_call_id="call_9ugEC0r5R0VPT2lYXt00Jyej",
      ),
      AIMessage(
        content="The following changes have been implemented:\n\n1. Added the `DUMMY` file to the template directory.\n2. Modified the `tsconfig.json` file in the template directory to remove the \"vitest.config.mts\" entry.\n\nThe\ntemplate is now updated to reflect the changes in the reference project.",
        additional_kwargs={"refusal": None},
        response_metadata={
          "token_usage": {
            "completion_tokens": 62,
            "prompt_tokens": 1112,
            "total_tokens": 1174,
            "completion_tokens_details": {
              "accepted_prediction_tokens": 0,
              "audio_tokens": None,
              "reasoning_tokens": None,
              "rejected_prediction_tokens": 0,
              "text_tokens": None,
            },
            "prompt_tokens_details": {
              "audio_tokens": None,
              "cache_write_tokens": None,
              "cached_tokens": 1024,
              "image_tokens": None,
              "text_tokens": None,
            },
          },
          "model_provider": "openai",
          "model_name": "gpt-4o-2024-11-20",
          "system_fingerprint": "fp_2b2e565915",
          "id": "chatcmpl-ERbyClxYKQEFZZe0z60KNw8iKu55y",
          "service_tier": "default",
          "finish_reason": "stop",
          "logprobs": None,
        },
        id="lc_run--01a0d32f-cd47-7cd0-be8a-771410f92a1c-0",
        tool_calls=[],
        invalid_tool_calls=[],
        usage_metadata={
          "input_tokens": 1112,
          "output_tokens": 62,
          "total_tokens": 1174,
          "input_token_details": {"cache_read": 1024},
          "output_token_details": {},
        },
      ),
    ]
  }

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
