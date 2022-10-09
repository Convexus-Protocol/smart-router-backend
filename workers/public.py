#!/usr/bin/env python

import uvicorn
from settings import PublicPoolsSettings

if __name__ == "__main__":
  uvicorn.run (
    "api.public.main:app",
    host=PublicPoolsSettings.host,
    port=PublicPoolsSettings.port,
    workers=1,
    reload=True
  )