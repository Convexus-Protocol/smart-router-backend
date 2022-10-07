import requests
import json

from database.models.pool import PoolsRead
from settings import PublicPoolsSettings

class Client:

  def __init__(self):
    self.endpoint = f"http://{PublicPoolsSettings.host}:{PublicPoolsSettings.port}"

  def pools_get_all(self) -> PoolsRead:
    return json.loads(requests.get(self.endpoint + "/pools/get_all").text)

  def tokens_get(self, address: str):
    return requests.get(self.endpoint + "/tokens/get", params={'token_address': address})
