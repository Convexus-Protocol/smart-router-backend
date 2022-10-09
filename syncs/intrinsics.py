import asyncio

from api.ticks.admin.client import Client as RestAdminClient
from database.models.sync import SyncSet
from syncs.base import SynchronizerBase
from syncs.eventlogs import IntrinsicsUpdate

from database.models.pool import IntrinsicsSet
from settings import BlockchainSettings, SynchronizerIntrinsicsSettings
from utils.sync import get_latest_height

rest_client = RestAdminClient()

class SynchronizerIntrinsics(SynchronizerBase):
  async def db_updater(self, queue: asyncio.Queue):
    height, eventlogs = await queue.get()
    
    for eventlog in eventlogs:
      # Parse event
      update = IntrinsicsUpdate.fromEventLog(eventlog)
      
      # Update Intrinsics DB
      intrinsicsSet = IntrinsicsSet(sqrtPriceX96=hex(update.sqrtPriceX96), tick=update.tick, liquidity=hex(update.liquidity), address=self.address)
      rest_client.intrinsics_set(intrinsicsSet)
      
    # Update Sync height DB
    syncCreate = SyncSet(name=SynchronizerIntrinsicsSettings.syncname, height=height)
    rest_client.syncs_set(syncCreate)

def start(address: str):
  # Read Sync latest height
  height = get_latest_height(rest_client, SynchronizerIntrinsicsSettings.syncname, address)

  # Start sync
  synchronizer = SynchronizerIntrinsics(
    BlockchainSettings.endpoint, 
    height,
    address,
    SynchronizerIntrinsicsSettings.event)

  return synchronizer.run()
