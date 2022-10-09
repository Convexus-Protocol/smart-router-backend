from fastapi import FastAPI
from api.admin.routers import syncs, tokens, pools, ticks
from api.dependencies import create_database

# Load DB
create_database()

# Load API
app = FastAPI()
app.include_router(syncs.router)
app.include_router(tokens.router)
app.include_router(pools.router)
app.include_router(ticks.router)