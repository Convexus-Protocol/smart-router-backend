from database.models.token import Token, TokenRead
from api.ticks.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter (
  prefix="/tokens",
  tags=["tokens"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.get("/get", response_model=TokenRead)
async def read_token(*, token_address: str):
  session = next(router.dependencies[0].dependency())
  token = session.get(Token, token_address)
  if not token:
    raise HTTPException(status_code=404, detail="token not found")
  return token
