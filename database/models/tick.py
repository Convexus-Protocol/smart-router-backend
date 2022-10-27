from typing import Optional
from sqlmodel import Field, SQLModel, Session
from sqlalchemy import exists

from utils.typing.bigint import BigInt
from convexus.sdk import Tick as TickSDK, TickConstructorArgs

class TickBase(SQLModel):
  index: int = Field(primary_key=True)
  liquidityNet: BigInt
  liquidityGross: BigInt

class Tick(TickBase, table=True):
  pool: Optional[str] = Field(default=None, foreign_key='pool.address', primary_key=True)

  @staticmethod
  def exists(session: Session, index: int, pool: str) -> bool:
    return session.query(exists().where(Tick.index==index, Tick.pool==pool)).scalar()

  def to_sdk(self):
    return TickSDK(TickConstructorArgs(self.index, self.liquidityGross, self.liquidityNet)) 

class TickGet(TickBase):
  pass

class TickSet(TickBase):
  pool: str

class TickDelete(SQLModel):
  index: int
  pool: str
