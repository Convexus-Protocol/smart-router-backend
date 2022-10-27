import asyncio

from api.admin.client import Client as RestAdminClient
from database.models.intrinsics import IntrinsicsSet
from database.models.sync import SyncSet
from syncs.base import SynchronizerBase
from convexus.sdk import IntrinsicsUpdate

from settings import BlockchainSettings, SynchronizerIntrinsicsSettings
from utils.sync import get_latest_height

rest_client = RestAdminClient()

class SynchronizerIntrinsics(SynchronizerBase):
  async def db_updater(self, queue: asyncio.Queue):
    block, eventlogs = await queue.get()
    
    for eventlog in eventlogs:
      # Parse event
      update = IntrinsicsUpdate.fromEventLog(eventlog)
      
      # Update Intrinsics DB
      intrinsicsSet = IntrinsicsSet(
        sqrtPriceX96=hex(update.sqrtPriceX96),
        tick=update.tick, 
        liquidity=hex(update.liquidity), 
        pool=self.address,
        timestamp=block['time_stamp'] // (1000 * 1000)
      )
      rest_client.intrinsics_set(intrinsicsSet)
      
    # Update Sync height DB
    syncCreate = SyncSet(name=SynchronizerIntrinsicsSettings.syncname, height=block['height'])
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

  asyncio.run(synchronizer.run())

