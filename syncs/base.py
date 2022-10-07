from asyncio import Queue
import asyncio
import json
import websockets
from abc import ABCMeta, abstractmethod
from loguru import logger

from utils.routerservice import RouterService

class SynchronizerBase(metaclass=ABCMeta):
  def __init__(self, endpoint: str, height: int, address: str, event: str) -> None:
    self.endpoint = endpoint
    self.height = height
    self.address = address
    self.event = event
    self.service = RouterService(endpoint)
    self.ws_to_chain = Queue()
    self.chain_to_db = Queue()

  async def ws_listener(self, queue: Queue):
    """
      Listen to the `TickUpdate` event and feed the websocket events to the `queue`
    """
    while True:
      try:
        async with websockets.connect(f"wss://{self.endpoint}/api/v3/icon_dex/event") as websocket:
          await websocket.send(json.dumps({
            "height": hex(self.height + 1),
            "addr": self.address,
            "event": self.event
          }))
          while True:
            packet = await websocket.recv()
            await queue.put(json.loads(packet))
            await asyncio.sleep(0.1)
      except Exception as e:
        logger.error(repr(e))

  async def blockchain_reader(self, inqueue, outqueue):
    """
      Listen to the event info in the `inqueue` and output the eventlog data to the `outqueue`
    """
    while True:
      try:
        data = await inqueue.get()
        if 'hash' in data:
          height = int(data['height'], 16) - 1 # -1 because we get notified during the next block
          block = self.service.icon.get_block(height)
          tx_index = int(data['index'], 16)
          txresult = self.service.icon.get_transaction_result(block['confirmed_transaction_list'][tx_index]['txHash'])
          for event in data['events']:
            self.height = height + 1
            await outqueue.put((self.height, txresult['eventLogs'][int(event, 16)]))
            await asyncio.sleep(0.1)
      except Exception as e:
        logger.error(repr(e))

  async def __db_updater(self, queue: asyncio.Queue):
    while True:
      try:
        await self.db_updater(queue)
        await asyncio.sleep(0.1)
      except Exception as e:
        logger.error(repr(e))

  @abstractmethod
  async def db_updater(self, queue: asyncio.Queue):
    """
      Listen to eventlogs in the `queue`, convert them to a SQL create/update query
    """
    pass

  async def run(self):    
    await asyncio.gather(
      asyncio.create_task(self.ws_listener(self.ws_to_chain)),
      asyncio.create_task(self.blockchain_reader(self.ws_to_chain, self.chain_to_db)),
      asyncio.create_task(self.__db_updater(self.chain_to_db))
    )
