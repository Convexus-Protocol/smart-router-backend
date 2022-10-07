from fastapi import FastAPI
from api.ticks.public.routers import tokens, pools, ticks, routing
from api.ticks.dependencies import create_database

# Load DB
create_database()

# Load API
app = FastAPI()
app.include_router(tokens.router)
app.include_router(pools.router)
app.include_router(ticks.router)
app.include_router(routing.router)