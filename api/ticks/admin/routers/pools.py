from database.models.pool import *
from api.ticks.dependencies import get_database_session
from fastapi import APIRouter, Depends
from sqlmodel import update

router = APIRouter (
  prefix="/pools",
  tags=["pools"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.post("/set")
def set_pool(*, pool: PoolSet):
  session = next(router.dependencies[0].dependency())

  if Pool.exists(session, pool.address):
    session.exec(update(Pool)
      .where(Pool.address==pool.address)
      .values(**pool.__dict__))
  else:
    session.add(Pool.from_orm(pool))

  session.commit()
  session.close()


@router.post("/intrinsics/set")
def set_pool_intrinsics(*, intrinsics: IntrinsicsSet):
  session = next(router.dependencies[0].dependency())

  if Pool.exists(session, intrinsics.address):
    session.exec(update(Pool)
      .where(Pool.address==intrinsics.address)
      .values(**intrinsics.__dict__))
    session.commit()

  session.close()