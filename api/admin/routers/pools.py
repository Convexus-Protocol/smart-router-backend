from database.models.pool import Pool, PoolSet
from api.dependencies import get_database_session
from fastapi import APIRouter, Depends

router = APIRouter (
  prefix="/pools",
  tags=["pools"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.post("/set")
def set_pool(*, pool: PoolSet):
  session = next(router.dependencies[0].dependency())
  session.add(Pool.from_orm(pool))

  try:
    session.commit()
  except:
    pass

  session.close()
