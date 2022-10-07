from database.models.tick import Tick as TickModel
from convexus.sdk import Tick, TickConstructorArgs

def tick_model_to_sdk(model: TickModel) -> Tick:
  if not model: return None
  return Tick(TickConstructorArgs(model.index, model.liquidityGross, model.liquidityNet)) 