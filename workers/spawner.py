import asyncio
from dataclasses import dataclass
from typing import Coroutine
from loguru import logger

from api.public.client import Client as RestPublicClient
from settings import SpawnerSettings
from syncs.pools import start as pools_start
from syncs.ticks import start as ticks_start
from syncs.intrinsics import start as intrinsics_start

logger.add(SpawnerSettings.logfile)

@dataclass
class PoolTask:
  coroutine: Coroutine
  address: str

def get_pool_addresses(result: dict) -> set:
  return set([pool['address'] for pool in result['pools']])

async def main():
  rest_client = RestPublicClient()

  # Create Pools Synchronizer tasks
  asyncio.create_task(pools_start())

  # Get list of pools for Ticks Synchronizer
  addresses = get_pool_addresses(rest_client.pools_get_all())

  # Create ticks + intrinsics synchronizers tasks
  for address in addresses:
    logger.info(f"Starting {address}")
    asyncio.create_task(ticks_start(address), name=address)
    asyncio.create_task(intrinsics_start(address), name=address)

  while True:
    await asyncio.sleep(SpawnerSettings.sleeptime)

    # Get list of new pools
    new_addresses = get_pool_addresses(rest_client.pools_get_all())
    # Spawn new addresses
    diff_addresses = new_addresses.difference(addresses)
    for address in diff_addresses:
      logger.info(f"Spawning new {address}")
      asyncio.create_task(ticks_start(address))
      asyncio.create_task(intrinsics_start(address))

    addresses = new_addresses

if __name__ == '__main__':
  asyncio.run(main())
