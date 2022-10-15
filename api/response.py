from typing import List
from convexus.icontoolkit.constants import BigintIsh
from pydantic import BaseModel

from convexus.sdk import Trade as TradeSDK
from convexus.sdk import RouteInfo as RouteInfoSDK
from convexus.sdk import Route as RouteSDK
from convexus.sdk import Token as TokenSDK
from convexus.sdk import Pool as PoolSDK
from convexus.sdk import CurrencyAmount as CurrencyAmountSDK

class Token(BaseModel):
  address: str
  decimals: int
  name: str
  symbol: str
  
  @staticmethod
  def from_sdk(token: TokenSDK) -> 'Token':
    return Token(
      address=token.address,
      decimals=token.decimals,
      name=token.name,
      symbol=token.symbol
    )

class Pool(BaseModel):
  token0: Token
  token1: Token
  fee: int
  sqrtRatioX96: BigintIsh
  liquidity: BigintIsh
  tickCurrent: int

  @staticmethod
  def from_sdk(pool: PoolSDK) -> 'Pool':
    return Pool(
      token0=Token.from_sdk(pool.token0),
      token1=Token.from_sdk(pool.token1),
      fee=pool.fee,
      sqrtRatioX96=hex(pool.sqrtRatioX96),
      liquidity=hex(pool.liquidity),
      tickCurrent=pool.tickCurrent
    )

class Route(BaseModel):
  pools: List[Pool]
  tokenPath: List[Token]
  input: Token
  output: Token
  
  @staticmethod
  def from_sdk(route: RouteSDK) -> 'Route':
    return Route(
      pools=list(map(Pool.from_sdk, route.pools)),
      tokenPath=list(map(Token.from_sdk, route.tokenPath)),
      input=Token.from_sdk(route.input),
      output=Token.from_sdk(route.output)
    )

class CurrencyAmount(BaseModel):
  numerator: BigintIsh
  denominator: BigintIsh
  currency: Token
  decimalScale: BigintIsh

  @staticmethod
  def from_sdk(amount: CurrencyAmountSDK) -> 'CurrencyAmount':
    return CurrencyAmount(
      numerator=hex(amount.numerator),
      denominator=hex(amount.denominator),
      currency=Token.from_sdk(amount.currency),
      decimalScale=hex(amount.decimalScale)
    )

class RouteInfo(BaseModel):
  route: Route
  inputAmount: CurrencyAmount
  outputAmount: CurrencyAmount
  
  @staticmethod
  def from_sdk(swap: RouteInfoSDK) -> 'RouteInfo':
    return RouteInfo(
      route=Route.from_sdk(swap.route),
      inputAmount=CurrencyAmount.from_sdk(swap.inputAmount),
      outputAmount=CurrencyAmount.from_sdk(swap.outputAmount),
    )

class Trade(BaseModel):
  swaps: List[RouteInfo]
  tradeType: int
  
  @staticmethod
  def from_sdk(trade: TradeSDK) -> 'Trade':
    return Trade(
      swaps=list(map(RouteInfo.from_sdk, trade.swaps)),
      tradeType=int(trade.tradeType.value)
    )
