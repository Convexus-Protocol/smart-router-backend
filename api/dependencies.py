from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///database/db/ticks.db", connect_args={"check_same_thread": False})

def get_database_session():
  with Session(engine) as session:
    yield session

def create_database():
  SQLModel.metadata.create_all(engine)