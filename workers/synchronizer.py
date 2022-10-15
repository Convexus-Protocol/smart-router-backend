import asyncio, multiprocessing
from typing import List
from loguru import logger
from api.public.client import Client as RestPublicClient
from database.models.pool import PoolGet
from settings import SpawnerSettings
from syncs.pools import start as pools_start
from syncs.ticks import start as ticks_start
from syncs.intrinsics import start as intrinsics_start

logger.add(SpawnerSettings.logfile)

def create_pools_process():
  multiprocessing.Process(target=pools_start).start()

def create_ticks_process(address):
  multiprocessing.Process(target=ticks_start, args=(address,)).start()

def create_intrinsics_process(address):
  multiprocessing.Process(target=intrinsics_start, args=(address,)).start()

def get_pool_addresses(result: List[PoolGet]) -> set:
  return set([pool.address for pool in result])

async def main():
  rest_client = RestPublicClient()

  # Create Pools Synchronizer tasks
  create_pools_process()

  # Get list of pools for Ticks Synchronizer
  addresses = get_pool_addresses(rest_client.pools_get_all())

  # Create ticks + intrinsics synchronizers tasks
  for address in addresses:
    logger.info(f"Starting {address}")
    create_ticks_process(address)
    create_intrinsics_process(address)

  while True:
    await asyncio.sleep(SpawnerSettings.sleeptime)

    # Get list of new pools
    new_addresses = get_pool_addresses(rest_client.pools_get_all())
    # Spawn new addresses
    diff_addresses = new_addresses.difference(addresses)
    for address in diff_addresses:
      logger.info(f"Spawning new {address}")
      create_ticks_process(address)
      create_intrinsics_process(address)

    addresses = new_addresses

if __name__ == '__main__':
  asyncio.run(main())