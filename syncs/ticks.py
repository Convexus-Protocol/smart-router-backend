import asyncio

from api.admin.client import Client as RestAdminClient
from database.models.sync import SyncSet
from syncs.base import SynchronizerBase
from syncs.eventlogs import TickUpdate

from database.models.tick import TickSet, TickDelete
from settings import BlockchainSettings, SynchronizerTicksSettings
from utils.sync import get_latest_height

rest_client = RestAdminClient()

class SynchronizerTicks(SynchronizerBase):
  async def db_updater(self, queue: asyncio.Queue):
    height, eventlogs = await queue.get()
    
    for eventlog in eventlogs:
      # Parse event
      tickUpdate = TickUpdate.fromEventLog(eventlog)
      
      # Update Tick DB
      if tickUpdate.initialized:
        # If initialized, create/update it
        tickSet = TickSet(
          index=tickUpdate.index, 
          liquidityNet=hex(tickUpdate.liquidityNet), 
          liquidityGross=hex(tickUpdate.liquidityGross),
          poolAddress=self.address)
        rest_client.ticks_set(tickSet)
      else:
        # If not initialized, delete it as it's not relevant anymore for routing
        tickDelete = TickDelete(index=tickUpdate.index, poolAddress=self.address)
        rest_client.ticks_delete(tickDelete)
        
    # Update Sync height DB
    syncCreate = SyncSet(name=SynchronizerTicksSettings.syncname, height=height)
    rest_client.syncs_set(syncCreate)

def start(address: str):
  # Read Sync latest height
  height = get_latest_height(rest_client, SynchronizerTicksSettings.syncname, address)

  synchronizer = SynchronizerTicks(
    BlockchainSettings.endpoint, 
    height,
    address,
    SynchronizerTicksSettings.event)

  asyncio.run(synchronizer.run())

