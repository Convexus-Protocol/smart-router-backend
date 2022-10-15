import asyncio

from api.public.client import Client as RestPublicClient
from api.admin.client import Client as RestAdminClient
from database.models.sync import SyncSet
from database.models.token import TokenSet
from syncs.base import SynchronizerBase

from database.models.pool import PoolSet
from settings import BlockchainSettings, SynchronizerPoolsSettings
from utils.sync import get_latest_height

from convexus.sdk import IIRC2, Token, PoolCreated
from convexus.icontoolkit import Contract

rest_public_client = RestPublicClient()
rest_admin_client = RestAdminClient()

class SynchronizerPools(SynchronizerBase):

  async def tokens_set(self, address: str):
    # Check if already in DB
    if rest_public_client.tokens_get(address).status_code == 404:
      # Get Tokens information from contract
      contract = Contract(address, IIRC2, self.service.icon, self.service.icon, 0)
      token = await Token.fromContract(contract)
      # Update DB
      rest_admin_client.tokens_set(TokenSet(address=token.address, decimals=token.decimals, name=token.name, symbol=token.symbol))

  async def db_updater(self, queue: asyncio.Queue):
    block, eventlogs = await queue.get()
    
    for eventlog in eventlogs:
      # Parse event
      poolCreated = PoolCreated.fromEventLog(eventlog)
      
      # Update Pool DB
      poolSet = PoolSet(
        address=poolCreated.pool, 
        token0=poolCreated.token0, 
        token1=poolCreated.token1, 
        fee=poolCreated.fee)
      rest_admin_client.pools_set(poolSet)
      
      # Create tokens if not already in DB
      asyncio.create_task(self.tokens_set(poolSet.token0))
      asyncio.create_task(self.tokens_set(poolSet.token1))

    # Update Sync height DB
    syncSet = SyncSet(name=SynchronizerPoolsSettings.syncname, height=block['height'])
    rest_admin_client.syncs_set(syncSet)
      
def start():
  # Read Sync latest height
  height = get_latest_height(rest_admin_client, SynchronizerPoolsSettings.syncname, SynchronizerPoolsSettings.factoryAddress)

  synchronizer = SynchronizerPools(
    BlockchainSettings.endpoint, 
    height, 
    SynchronizerPoolsSettings.factoryAddress, 
    SynchronizerPoolsSettings.event
  )

  asyncio.run(synchronizer.run())

