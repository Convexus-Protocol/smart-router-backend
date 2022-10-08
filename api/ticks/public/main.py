from fastapi import FastAPI
from api.ticks.public.routers import tokens, pools, ticks, routing
from api.ticks.dependencies import create_database
from fastapi.middleware.cors import CORSMiddleware

# Load DB
create_database()

# Load API
app = FastAPI()

origins = [
  "http://localhost:8080",
  "https://convexus-sdk-js-webpack-boilerplate.pages.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tokens.router)
app.include_router(pools.router)
app.include_router(ticks.router)
app.include_router(routing.router)