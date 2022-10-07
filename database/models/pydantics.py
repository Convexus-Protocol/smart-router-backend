from typing import List
from convexus.icontoolkit.constants import BigintIsh
from sqlmodel import SQLModel

from convexus.sdk import Trade as TradeSDK
from convexus.sdk import RouteInfo as RouteInfoSDK
from convexus.sdk import Route as RouteSDK
from convexus.sdk import Token as TokenSDK
from convexus.sdk import Pool as PoolSDK
from convexus.sdk import CurrencyAmount as CurrencyAmountSDK

class Token(SQLModel):
  address: str
  decimals: int
  name: str
  symbol: str

class Pool(SQLModel):
  token0: Token
  token1: Token
  fee: int
  sqrtRatioX96: BigintIsh
  liquidity: BigintIsh
  tickCurrent: int

class Route(SQLModel):
  pools: List[Pool]
  tokenPath: List[Token]
  input: Token
  output: Token

class CurrencyAmount(SQLModel):
  numerator: BigintIsh
  denominator: BigintIsh
  currency: Token
  decimalScale: BigintIsh

class RouteInfo(SQLModel):
  route: Route
  inputAmount: CurrencyAmount
  outputAmount: CurrencyAmount

class Trade(SQLModel):
  swaps: List[RouteInfo]


def currencyamount_sdk_to_model(amount: CurrencyAmountSDK) -> CurrencyAmount:
  return CurrencyAmount(
    numerator=hex(amount.numerator),
    denominator=hex(amount.denominator),
    currency=token_sdk_to_model(amount.currency),
    decimalScale=hex(amount.decimalScale)
  )

def token_sdk_to_model(token: TokenSDK) -> Token:
  return Token(
    address=token.address,
    decimals=token.decimals,
    name=token.name,
    symbol=token.symbol
  )

def pool_sdk_to_model(pool: PoolSDK) -> Pool:
  return Pool(
    token0=token_sdk_to_model(pool.token0),
    token1=token_sdk_to_model(pool.token1),
    fee=pool.fee,
    sqrtRatioX96=hex(pool.sqrtRatioX96),
    liquidity=hex(pool.liquidity),
    tickCurrent=pool.tickCurrent
  )

def route_sdk_to_model(route: RouteSDK) -> Route:
  return Route(
    pools=list(map(pool_sdk_to_model, route.pools)),
    tokenPath=list(map(token_sdk_to_model, route.tokenPath)),
    input=token_sdk_to_model(route.input),
    output=token_sdk_to_model(route.output)
  )

def routeinfo_sdk_to_model(swap: RouteInfoSDK) -> RouteInfo:
  return RouteInfo(
    route=route_sdk_to_model(swap.route),
    inputAmount=currencyamount_sdk_to_model(swap.inputAmount),
    outputAmount=currencyamount_sdk_to_model(swap.outputAmount),
  )

def trade_sdk_to_model(trade: TradeSDK) -> Trade:
  return Trade(
    swaps=list(map(routeinfo_sdk_to_model, trade.swaps))
  )