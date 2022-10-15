from typing import List
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import Field, SQLModel, Session, Relationship
from sqlalchemy import exists
from database.models.intrinsics import Intrinsics
from database.models.tick import Tick

from convexus.icontoolkit import BigintIsh
from convexus.sdkcore import Token as TokenSDK
from convexus.sdk import Pool as PoolSDK, NoTickDataProvider

from utils.typing.bigint import BigInt

class PoolBase(SQLModel):
  address: str = Field(primary_key=True)
  token0: str = Field(foreign_key='token.address')
  token1: str = Field(foreign_key='token.address')
  fee: int

class Pool(PoolBase, SQLModel, table=True):
  ticks: List[Tick] = Relationship()

  @staticmethod
  def exists(session: Session, address: str) -> bool:
    return session.query(exists().where(Pool.address==address)).scalar()

  def to_sdk (
    self, 
    token0: TokenSDK, token1: TokenSDK,
    sqrtPriceX96: BigintIsh,
    liquidity: BigintIsh,
    currentTick: int,
    ticks: List[Tick] = NoTickDataProvider()
  ) -> PoolSDK:
    return PoolSDK (
      token0, token1, 
      self.fee, 
      sqrtPriceX96,
      liquidity,
      currentTick,
      ticks
    )

class PoolGet(PoolBase):
  sqrtPriceX96: BigInt
  tick: int
  liquidity: BigInt

class PoolSet(PoolBase):
  pass
