from database.models.token import TokenSet, Token
from api.ticks.dependencies import get_database_session
from fastapi import APIRouter, Depends
from sqlmodel import update

router = APIRouter (
  prefix="/tokens",
  tags=["tokens"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

@router.post("/set")
def set_token(*, token: TokenSet):
  session = next(router.dependencies[0].dependency())

  if Token.exists(session, token.address):
    session.exec(update(Token)
      .where(Token.address==token.address)
      .values(**token.__dict__))
  else:
    session.add(Token.from_orm(token))
  
  session.commit()
  session.close()
