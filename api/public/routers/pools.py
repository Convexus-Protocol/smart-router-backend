from typing import List
from database.models.intrinsics import Intrinsics, IntrinsicsBase
from database.models.pool import Pool, PoolGet
from api.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from sqlalchemy import desc

router = APIRouter (
  prefix="/pools",
  tags=["pools"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

def get_latest_intrinsics(session: Session, pool_address: str) -> IntrinsicsBase:
  try:
    intrinsics = session.exec(
      select(Intrinsics)
      .where(Intrinsics.pool == pool_address)
      .order_by(desc(Intrinsics.timestamp))
      .limit(1)
    ).one()
    return IntrinsicsBase(
      sqrtPriceX96=intrinsics.sqrtPriceX96,
      tick=intrinsics.tick,
      liquidity=intrinsics.liquidity
    )
  except:
    # The pool may not have been initialized yet
    return IntrinsicsBase(
      sqrtPriceX96=hex(0), 
      tick=0,
      liquidity=hex(0)
    )

@router.get("/get", response_model=PoolGet)
async def read_pool(*, pool_address: str):
  session = next(router.dependencies[0].dependency())
  pool = session.get(Pool, pool_address)
  if not pool:
    raise HTTPException(status_code=404, detail="pool not found")
  
  # Get latest intrinsics
  intrinsics = get_latest_intrinsics(session, pool_address)
  
  return PoolGet (
    **pool.__dict__, 
    **intrinsics.__dict__
  )

@router.get("/get_all", response_model=List[PoolGet])
async def read_pools():
  session = next(router.dependencies[0].dependency())
  pools = session.exec(select(Pool)).all()
  intrinsics = list(map(lambda r: get_latest_intrinsics(session, r), pools))
  return list(map(
    lambda pi: 
      PoolGet(
        **pi[0].__dict__, 
        **pi[1].__dict__
      ), 
    zip(pools, intrinsics)
  ))
