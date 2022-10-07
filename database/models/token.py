from typing import Optional
from sqlmodel import Field, SQLModel, Session
from sqlalchemy import exists

class TokenBase(SQLModel):
  address: str = Field(primary_key=True)
  decimals: int
  name: Optional[str] = Field(default=None)
  symbol: Optional[str] = Field(default=None)

class Token(TokenBase, table=True):

  @staticmethod
  def exists(session: Session, address: str) -> bool:
    return session.query(exists().where(Token.address==address)).scalar()

class TokenRead(TokenBase):
  pass

class TokenSet(TokenBase):
  pass
