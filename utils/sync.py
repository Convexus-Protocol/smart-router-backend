from api.ticks.admin.client import Client
from utils.score import score_initial_deployment
from database.models.sync import SyncSet
import json

def get_latest_height(rest_client: Client, syncname, address):
  sync = rest_client.syncs_get(syncname)
  if sync.status_code == 404:
    height = score_initial_deployment(address)
    rest_client.syncs_set(SyncSet(name=syncname, height=height))
  else:
    height = json.loads(sync.text)['height']

  return height