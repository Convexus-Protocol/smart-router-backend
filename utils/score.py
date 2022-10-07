from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

from settings import BlockchainSettings

def score_initial_deployment(address: str, height = None):
  icon_service = IconService(HTTPProvider(f"https://{BlockchainSettings.endpoint}", 3))
  try:
    status = icon_service.get_score_status(address, height)
  except:
    return height 
  deployTxHash = status['current']['deployTxHash']
  txResult = icon_service.get_transaction_result(deployTxHash)
  blockHeight = txResult['blockHeight']
  return score_initial_deployment(address, blockHeight)
