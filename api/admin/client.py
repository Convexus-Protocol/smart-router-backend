import requests
import json
from database.models.sync import SyncSet
from database.models.pool import IntrinsicsSet, PoolSet
from database.models.token import TokenSet
from database.models.tick import TickSet, TickDelete
from settings import AdminPoolsSettings

class Client:

  def __init__(self):
    self.endpoint = f"http://{AdminPoolsSettings.host}:{AdminPoolsSettings.port}"

  def syncs_get(self, name: str):
    return requests.get(self.endpoint + "/syncs/get", params={'name': name})

  def syncs_set(self, data: SyncSet):
    return requests.post(self.endpoint + "/syncs/set", data=json.dumps(data.__dict__))

  def pools_set(self, data: PoolSet):
    return requests.post(self.endpoint + "/pools/set", data=json.dumps(data.__dict__))

  def intrinsics_set(self, data: IntrinsicsSet):
    return requests.post(self.endpoint + "/pools/intrinsics/set", data=json.dumps(data.__dict__))

  def tokens_set(self, data: TokenSet):
    return requests.post(self.endpoint + "/tokens/set", data=json.dumps(data.__dict__))

  def ticks_set(self, data: TickSet):
    return requests.post(self.endpoint + "/ticks/set", data=json.dumps(data.__dict__))
    
  def ticks_delete(self, data: TickDelete):
    return requests.delete(self.endpoint + "/ticks/delete", data=json.dumps(data.__dict__))