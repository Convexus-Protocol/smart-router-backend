import asyncio

from api.ticks.public.client import Client as RestPublicClient
from api.ticks.admin.client import Client as RestAdminClient
from database.models.sync import SyncSet
from database.models.token import TokenSet
from syncs.base import SynchronizerBase
from syncs.eventlogs import PoolCreated

from database.models.pool import PoolSet
from settings import BlockchainSettings, SynchronizerPoolsSettings
from utils.sync import get_latest_height

from convexus.sdk import IIRC2, Token
from convexus.icontoolkit import Contract

rest_public_client = RestPublicClient()
rest_admin_client = RestAdminClient()

class SynchronizerPools(SynchronizerBase):

  async def tokens_set(self, address: str):
    if rest_public_client.tokens_get(address).status_code == 404:
      contract = Contract(address, IIRC2, self.service.icon, self.service.icon, 0)
      token = await Token.fromContract(contract)
      rest_admin_client.tokens_set(TokenSet(address=token.address, decimals=token.decimals, name=token.name, symbol=token.symbol))

  async def db_updater(self, queue: asyncio.Queue):
    height, eventlog = await queue.get()
    poolCreated = PoolCreated.fromEventLog(eventlog)
    poolSet = PoolSet(
      address=poolCreated.pool, 
      token0=poolCreated.token0, 
      token1=poolCreated.token1, 
      fee=poolCreated.fee)
    syncSet = SyncSet(name=SynchronizerPoolsSettings.syncname, height=height)
    rest_admin_client.pools_set(poolSet)
    rest_admin_client.syncs_set(syncSet)
    asyncio.create_task(self.tokens_set(poolSet.token0))
    asyncio.create_task(self.tokens_set(poolSet.token1))

def start():
  height = get_latest_height(rest_admin_client, SynchronizerPoolsSettings.syncname, SynchronizerPoolsSettings.address)

  synchronizer = SynchronizerPools(
    BlockchainSettings.endpoint, 
    height, 
    SynchronizerPoolsSettings.address, 
    SynchronizerPoolsSettings.event
  )

  return synchronizer.run()

