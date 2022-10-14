from dataclasses import dataclass

@dataclass
class PublicPoolsSettings:
  host: str = "127.0.0.1"
  port: int = 8000

@dataclass
class AdminPoolsSettings:
  host: str = "127.0.0.1"
  port: int = 8001

@dataclass
class BlockchainSettings:
  endpoint: str = "berlin.net.solidwallet.io"

@dataclass
class SynchronizerPoolsSettings:
  factoryAddress: str = "cx5e0f1b97cfb7b2c83950200b2bc5cb723bb80694"
  event: str = "PoolCreated(Address,Address,int,int,Address)"
  syncname: str = "pools"

@dataclass
class SynchronizerTicksSettings:
  event: str = "TickUpdate(int,int,int,int,int,int,int,int,bool)"
  syncname: str = "ticks"

@dataclass
class SynchronizerIntrinsicsSettings:
  event: str = "PoolIntrinsicsUpdate(int,int,int)"
  syncname: str = "intrinsics"

@dataclass
class SpawnerSettings:
  sleeptime: int = 1
  logfile: str = "logs/spawner_ticks.log"