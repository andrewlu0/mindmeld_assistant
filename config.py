PARSER_CONFIG = {
    'field': ['customer_id', 'number', 'contact_type'],
}

action_map = {
  "create": {
    "viewActionParam": "&viewAction=CREATE",
    "viewModeParam": "&hybridMode=maint",
  },
  "read": {
    "viewActionParam": "",
    "viewModeParam": "&hybridMode=browse",
  },
  "update": {
    "viewActionParam": "&viewAction=UPDATE",
    "viewModeParam": "&hybridMode=hybrid",
  },
  "delete": {
    "viewActionParam": "&viewAction=DELETE",
    "viewModeParam": "&hybridMode=hybrid",
  }
}

base_url = "https://qvarfrdlwb01.qad.com/clouderp/#/view/qraview/hybridbrowse?viewMetaUri=urn:view:meta:com.qad.erp."

def get_view_params(action):
    return action_map[action]["viewActionParam"], action_map[action]["viewModeParam"]