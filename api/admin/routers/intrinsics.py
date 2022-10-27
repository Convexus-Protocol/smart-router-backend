from database.models.intrinsics import Intrinsics, IntrinsicsSet
from api.dependencies import get_database_session
from fastapi import APIRouter, Depends

router = APIRouter (
  prefix="/intrinsics",
  tags=["intrinsics"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.post("/set")
def set_intrinsics(*, intrinsics: IntrinsicsSet):
  session = next(router.dependencies[0].dependency())
  session.add(Intrinsics.from_orm(intrinsics))
  session.commit()
  session.close()