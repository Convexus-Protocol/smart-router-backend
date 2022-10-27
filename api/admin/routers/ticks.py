from database.models.tick import Tick, TickSet, TickDelete
from api.dependencies import get_database_session
from fastapi import APIRouter, Depends
from sqlmodel import update, delete

router = APIRouter (
  prefix="/ticks",
  tags=["ticks"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.post("/set")
def set_tick(*, tick: TickSet):
  session = next(router.dependencies[0].dependency())

  if Tick.exists(session, tick.index, tick.pool):
    session.exec(update(Tick)
      .where(Tick.index == tick.index, Tick.pool == tick.pool)
      .values(liquidityNet=tick.liquidityNet, liquidityGross=tick.liquidityGross))
  else:
    session.add(Tick.from_orm(tick))

  try:
    session.commit()
  except:
    pass

  session.close()


@router.delete("/delete")
def delete_tick(*, tick: TickDelete):
  session = next(router.dependencies[0].dependency())
  session.exec(delete(Tick)
    .where(Tick.index == tick.index, Tick.pool == tick.pool))
  session.commit()
  session.close()