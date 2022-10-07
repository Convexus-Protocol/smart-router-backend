from database.models.sync import Sync, SyncRead, SyncSet
from api.ticks.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import update

router = APIRouter (
  prefix="/syncs",
  tags=["syncs"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.get("/get", response_model=SyncRead)
async def read_sync(*, name: str):
  session = next(router.dependencies[0].dependency())
  sync = session.get(Sync, name)
  if not sync:
    raise HTTPException(status_code=404, detail="sync not found")
  return sync

@router.post("/set")
def set_sync(*, sync: SyncSet):
  session = next(router.dependencies[0].dependency())

  if Sync.exists(session, sync.name):
    session.exec(update(Sync)
      .where(Sync.name==sync.name)
      .values(**sync.__dict__))
  else:
    session.add(Sync.from_orm(sync))
  
  session.commit()
  session.close()
