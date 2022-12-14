from typing import Dict, List
from database.models.intrinsics import Intrinsics
from database.models.pool import Pool as PoolModel
from api.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from convexus.sdk import Trade, Pool, PoolFactoryProvider, Token, FeeAmount, CurrencyAmount, BestTradeOptions
from api.response import Trade as TradeResponse
from database.models.token import Token as TokenModel
from sqlalchemy import desc

router = APIRouter (
  prefix="/routing",
  tags=["routing"],
  responses={404: {"description": "Not found"}},
  dependencies=[Depends(get_database_session)]
)

class RoutingPoolFactoryProvider(PoolFactoryProvider):
  def __init__(self, pools: Dict[str, Pool]) -> None:
    super().__init__()
    self.pools = pools
  
  def getPool (
    self,
    tokenA: Token,
    tokenB: Token,
    fee: FeeAmount
  ) -> str:
    tokenA, tokenB = [tokenA, tokenB] if tokenA.sortsBefore(tokenB) else [tokenB, tokenA]
    for address, pool in self.pools.items():
      if pool.token0.equals(tokenA) and pool.token1.equals(tokenB) and pool.fee == fee:
        return address

    raise Exception("Pool not found")


@router.get("/bestTradeExactIn/{currencyInAddress}/{currencyOutAddress}/{currencyAmountIn}", response_model=List[TradeResponse])
async def bestTradeExactIn(*, currencyInAddress: str, currencyOutAddress: str, currencyAmountIn: int):
  session = next(router.dependencies[0].dependency())

  tokenIn: TokenModel = session.get(TokenModel, currencyInAddress)
  tokenOut: TokenModel = session.get(TokenModel, currencyOutAddress)

  if not tokenIn:
    raise HTTPException(status_code=404, detail="tokenIn not found")

  if not tokenOut:
    raise HTTPException(status_code=404, detail="tokenOut not found")

  # Convert to SDK objects
  tokenIn = tokenIn.to_sdk()
  tokenOut = tokenOut.to_sdk()

  # Get all pools
  db_pools: List[PoolModel] = session.exec(select(PoolModel)).all()

  pools = {}
  for db_pool in db_pools:
    # Convert TokenModel to SDK Token
    token0: Token = session.get(TokenModel, db_pool.token0).to_sdk()
    token1: Token = session.get(TokenModel, db_pool.token1).to_sdk()

    # Convert TicksModel to SDK Ticks
    ticks = list(map(lambda t: t.to_sdk(), db_pool.ticks))
    # Sort ticks
    ticks = sorted(ticks, key=lambda x: x.index)

    # Get latest intrinsics
    try:
      intrinsics: Intrinsics = session.exec(
        select(Intrinsics)
        .where(Intrinsics.pool == db_pool.address)
        .order_by(desc(Intrinsics.timestamp))
        .limit(1)
      ).one()
    except:
      # The pool may not have been initialized yet
      continue

    # Convert PoolModel to SDK Pool if any tick
    if ticks:
      pools[db_pool.address] = db_pool.to_sdk(
        token0, token1, 
        intrinsics.sqrtPriceX96, 
        intrinsics.liquidity, 
        intrinsics.tick,
        ticks
      )

  if not len(pools):
    raise HTTPException(status_code=404, detail="Pools not found")

  poolProvider = RoutingPoolFactoryProvider(pools)
  currencyAmountIn = CurrencyAmount(tokenIn, currencyAmountIn)
  trades = Trade.bestTradeExactIn(poolProvider, list(pools.values()), currencyAmountIn=currencyAmountIn, currencyOut=tokenOut, options=BestTradeOptions(maxHops=4))

  # Convert SDK to Pydantic
  return list(map(TradeResponse.from_sdk, trades))