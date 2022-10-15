from typing import Optional
from sqlmodel import Field, SQLModel
from utils.typing.bigint import BigInt
from datetime import datetime

class IntrinsicsBase(SQLModel):
  sqrtPriceX96: BigInt
  tick: int
  liquidity: BigInt

class Intrinsics(IntrinsicsBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  pool: str = Field(foreign_key='pool.address', index=True)
  timestamp: datetime = Field(index=True)

class IntrinsicsSet(IntrinsicsBase):
  pool: str
  timestamp: int

class IntrinsicsGet(IntrinsicsBase):
  timestamp: int
