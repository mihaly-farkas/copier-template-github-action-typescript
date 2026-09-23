import json
from conf import WORKFLOW_STATE_JSON_PATH
from helper.json_encoder import JsonEncoder


def save_workflow_state(state):
  state_file_content = json.dumps(state, indent=2, ensure_ascii=False, cls=JsonEncoder)
  WORKFLOW_STATE_JSON_PATH.write_text(state_file_content, encoding="utf-8")
