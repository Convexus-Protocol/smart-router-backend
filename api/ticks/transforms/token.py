from database.models.token import Token as TokenModel
from convexus.sdk import Token

def token_model_to_sdk(model: TokenModel) -> Token:
  if not model: return None
  return Token(model.address, model.decimals, model.symbol, model.name)