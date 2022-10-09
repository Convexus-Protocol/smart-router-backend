from typing import List, Optional
from sqlmodel import Field, SQLModel, Session, Relationship
from sqlalchemy import exists

from database.models.tick import Tick, TickRead
from utils.typing.bigint import BigInt

from convexus.sdkcore import Token as TokenSDK
from convexus.sdk import Pool as PoolSDK, NoTickDataProvider

class IntrinsicsBase(SQLModel):
  sqrtPriceX96: Optional[BigInt] = Field(default=None)
  tick: Optional[int] = Field(default=None)
  liquidity: Optional[BigInt] = Field(default=None)

class PoolBase(IntrinsicsBase, SQLModel):
  address: str = Field(primary_key=True)
  token0: str = Field(foreign_key='token.address')
  token1: str = Field(foreign_key='token.address')
  fee: int

class Pool(PoolBase, SQLModel, table=True):
  ticks: List['Tick'] = Relationship()

  @staticmethod
  def exists(session: Session, address: str) -> bool:
    return session.query(exists().where(Pool.address==address)).scalar()

  def to_sdk (
    self, 
    token0: TokenSDK, token1: TokenSDK, 
    ticks: List[Tick] = NoTickDataProvider()
  ) -> PoolSDK:
    return PoolSDK (
      token0, token1, 
      self.fee, 
      self.sqrtPriceX96, 
      self.liquidity, 
      self.tick, 
      ticks
    )

class PoolRead(PoolBase):
  pass

class PoolReadWithTicks(PoolRead):
  ticks: List['TickRead'] = []

class PoolsRead(SQLModel):
  pools: List['PoolRead']

class PoolSet(PoolBase):
  pass

class IntrinsicsSet(IntrinsicsBase):
  address: str