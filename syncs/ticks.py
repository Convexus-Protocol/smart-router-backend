import asyncio

from api.ticks.admin.client import Client as RestAdminClient
from database.models.sync import SyncSet
from syncs.base import SynchronizerBase
from syncs.eventlogs import TickUpdate

from database.models.tick import TickSet, TickDelete
from settings import BlockchainSettings, SynchronizerTicksSettings
from utils.sync import get_latest_height

rest_client = RestAdminClient()

class SynchronizerTicks(SynchronizerBase):
  async def db_updater(self, queue: asyncio.Queue):
    height, eventlog = await queue.get()
    tickUpdate = TickUpdate.fromEventLog(eventlog)
    if tickUpdate.initialized:
      tickSet = TickSet(
        index=tickUpdate.index, 
        liquidityNet=hex(tickUpdate.liquidityNet), 
        liquidityGross=hex(tickUpdate.liquidityGross),
        poolAddress=self.address)
      rest_client.ticks_set(tickSet)
    else:
      tickDelete = TickDelete(index=tickUpdate.index, poolAddress=self.address)
      rest_client.ticks_delete(tickDelete)
    syncCreate = SyncSet(name=SynchronizerTicksSettings.syncname, height=height+1)
    rest_client.syncs_set(syncCreate)

def start(address: str):
  height = get_latest_height(rest_client, SynchronizerTicksSettings.syncname, address)

  synchronizer = SynchronizerTicks(
    BlockchainSettings.endpoint, 
    height,
    address,
    SynchronizerTicksSettings.event)

  return synchronizer.run()
