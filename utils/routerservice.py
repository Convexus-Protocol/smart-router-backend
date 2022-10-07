from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from utils.asynchronous import make_async

class RouterService:
  def __init__(self, endpoint: str) -> None:
    self.icon = self.get_icon_service(endpoint)

  def get_icon_service(self, endpoint: str):
    return IconService(HTTPProvider(f"https://{endpoint}", 3))
