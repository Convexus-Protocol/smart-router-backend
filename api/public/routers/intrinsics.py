from datetime import datetime
from typing import List
from database.models.intrinsics import Intrinsics, IntrinsicsGet
from api.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

router = APIRouter (
  prefix="/intrinsics",
  tags=["intrinsics"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.get("/get", response_model=List[IntrinsicsGet])
async def read_intrinsics(*, pool_address: str, timestamp: int, offset: int = 0):
  session = next(router.dependencies[0].dependency())
  intrinsics: Intrinsics = session.exec(
    select(Intrinsics)
    .where(Intrinsics.pool==pool_address, Intrinsics.timestamp >= datetime.fromtimestamp(timestamp))
    .offset(offset)
    .limit(1000)
  ).all()
  if not intrinsics:
    raise HTTPException(status_code=404, detail="intrinsics not found")
  return list(map(lambda i: 
    IntrinsicsGet(
      sqrtPriceX96=i.sqrtPriceX96, 
      tick=i.tick, 
      liquidity=i.liquidity, 
      timestamp=datetime.timestamp(i.timestamp)
    ),
    intrinsics
  ))