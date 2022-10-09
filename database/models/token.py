from typing import Optional
from sqlmodel import Field, SQLModel, Session
from sqlalchemy import exists

from convexus.sdkcore import Token as TokenSDK

class TokenBase(SQLModel):
  address: str = Field(primary_key=True)
  decimals: int
  name: Optional[str] = Field(default=None)
  symbol: Optional[str] = Field(default=None)

class Token(TokenBase, table=True):

  @staticmethod
  def exists(session: Session, address: str) -> bool:
    return session.query(exists().where(Token.address==address)).scalar()

  def to_sdk(self):
    return TokenSDK(self.address, self.decimals, self.symbol, self.name)

class TokenRead(TokenBase):
  pass

class TokenSet(TokenBase):
  pass
