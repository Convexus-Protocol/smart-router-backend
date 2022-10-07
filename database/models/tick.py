from typing import Optional
from sqlmodel import Field, SQLModel, Session
from sqlalchemy import exists

from utils.typing.bigint import BigInt

class TickBase(SQLModel):
  index: int = Field(primary_key=True)
  liquidityNet: BigInt
  liquidityGross: BigInt

class Tick(TickBase, table=True):
  poolAddress: Optional[str] = Field(default=None, foreign_key='pool.address', primary_key=True)

  @staticmethod
  def exists(session: Session, index: int, poolAddress: str) -> bool:
    return session.query(exists().where(Tick.index==index, Tick.poolAddress==poolAddress)).scalar()

class TickRead(TickBase):
  pass

class TickSet(TickBase):
  poolAddress: str

class TickDelete(SQLModel):
  index: int
  poolAddress: str
