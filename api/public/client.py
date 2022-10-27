from typing import List
import requests
import json

from database.models.pool import PoolGet
from settings import PublicPoolsSettings

class Client:

  def __init__(self):
    self.endpoint = f"http://{PublicPoolsSettings.host}:{PublicPoolsSettings.port}"

  def pools_get_all(self) -> List[PoolGet]:
    return list(map(
      lambda x: PoolGet(**x),
      json.loads(requests.get(self.endpoint + "/pools/").text)))

  def tokens_get(self, address: str):
    return requests.get(self.endpoint + f"/tokens/{address}")
