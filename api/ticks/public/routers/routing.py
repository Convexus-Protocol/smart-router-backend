from typing import Dict, List
from api.ticks.transforms.pool import pool_model_to_sdk
from api.ticks.transforms.tick import tick_model_to_sdk
from api.ticks.transforms.token import token_model_to_sdk
from database.models.pool import Pool as PoolModel
from api.ticks.dependencies import get_database_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from convexus.sdk import Trade, Pool, PoolFactoryProvider, Token, FeeAmount, CurrencyAmount
from database.models.pydantics import trade_sdk_to_model, Trade as TradeModel
from database.models.token import Token as TokenModel


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


@router.get("/bestTradeExactIn", response_model=List[TradeModel])
async def bestTradeExactIn(*, currencyInAddress: str, currencyOutAddress: str, currencyAmountIn: int):
  session = next(router.dependencies[0].dependency())

  tokenIn = token_model_to_sdk(session.get(TokenModel, currencyInAddress))
  tokenOut = token_model_to_sdk(session.get(TokenModel, currencyOutAddress))
  
  if not tokenIn:
    raise HTTPException(status_code=404, detail="tokenIn not found")
  
  if not tokenOut:
    raise HTTPException(status_code=404, detail="tokenOut not found")
  
  # Get all pools
  db_pools: List[PoolModel] = session.exec(select(PoolModel)).all()
  
  pools = {}
  for db_pool in db_pools:
    # Convert TokenModel to SDK Token
    token0 = token_model_to_sdk(session.get(TokenModel, db_pool.token0))
    token1 = token_model_to_sdk(session.get(TokenModel, db_pool.token1))

    # Convert TicksModel to SDK Ticks
    ticks = list(map(tick_model_to_sdk, db_pool.ticks))

    # Convert PoolModel to SDK Pool if any tick
    if ticks:
      print(f"ticks for {db_pool.address}")
      pools[db_pool.address] = pool_model_to_sdk(db_pool, token0, token1, ticks)
  
  print(len(pools))
  poolProvider = RoutingPoolFactoryProvider(pools)
  currencyAmountIn = CurrencyAmount(tokenIn, currencyAmountIn)
  trades = Trade.bestTradeExactIn(poolProvider, list(pools.values()), currencyAmountIn=currencyAmountIn, currencyOut=tokenOut)
  
  # Convert SDK to Pydantic
  return list(map(trade_sdk_to_model, trades))