import json
from datetime import datetime


class JsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj, '__dict__'):
      return obj.__dict__
    if isinstance(obj, datetime):
      return obj.isoformat()
    return super().default(obj)
