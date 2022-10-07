from database.models.pool import Pool, PoolRead, PoolReadWithTicks, PoolsRead
from api.ticks.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

router = APIRouter (
  prefix="/pools",
  tags=["pools"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.get("/get", response_model=PoolReadWithTicks)
async def read_pool(*, pool_address: str):
  session = next(router.dependencies[0].dependency())
  pool = session.get(Pool, pool_address)
  if not pool:
    raise HTTPException(status_code=404, detail="pool not found")
  return pool

@router.get("/get_all", response_model=PoolsRead)
async def read_pools():
  session = next(router.dependencies[0].dependency())
  result = session.exec(select(Pool)).all()
  return PoolsRead(pools=list(map(lambda pool: PoolRead(**pool.__dict__), result)))
