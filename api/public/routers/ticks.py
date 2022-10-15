from database.models.tick import Tick, TickGet
from api.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter (
  prefix="/ticks",
  tags=["ticks"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.get("/get", response_model=TickGet)
async def read_tick(*, pool_address: str, tick_index: int):
  session = next(router.dependencies[0].dependency())
  tick = session.get(Tick, (tick_index, pool_address))
  if not tick:
    raise HTTPException(status_code=404, detail="tick not found")
  return tick
