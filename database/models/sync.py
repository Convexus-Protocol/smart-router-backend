from sqlmodel import Field, SQLModel, Session
from sqlalchemy import exists

class SyncBase(SQLModel):
  height: int

class Sync(SyncBase, table=True):
  name: str = Field(primary_key=True)

  @staticmethod
  def exists(session: Session, name: str) -> bool:
    return session.query(exists().where(Sync.name==name)).scalar()

class SyncRead(SyncBase):
  pass

class SyncSet(SyncBase):
  name: str
