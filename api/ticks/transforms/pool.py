from typing import List
from database.models.pool import Pool as PoolModel
from convexus.sdk import Pool
from convexus.sdk import Pool, Token, Tick, PoolFactoryProvider, NoPoolFactoryProvider, NoTickDataProvider

def pool_model_to_sdk (
  model: PoolModel, 
  token0: Token, token1: Token, 
  ticks: List[Tick] = NoTickDataProvider()
) -> Pool:
  if not model: return None
  return Pool (
    token0, token1, 
    model.fee, 
    model.sqrtPriceX96, 
    model.liquidity, 
    model.tick, 
    ticks
  )
