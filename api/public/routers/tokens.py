from database.models.token import Token, TokenGet
from api.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter (
  prefix="/tokens",
  tags=["tokens"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.get("/{token_address}", response_model=TokenGet)
async def read_token(*, token_address: str):
  session = next(router.dependencies[0].dependency())
  token = session.get(Token, token_address)
  if not token:
    raise HTTPException(status_code=404, detail="token not found")
  return token
