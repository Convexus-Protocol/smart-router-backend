#!/usr/bin/env python

import uvicorn
from settings import AdminPoolsSettings

if __name__ == "__main__":
  uvicorn.run (
    "api.admin.main:app",
    host=AdminPoolsSettings.host,
    port=AdminPoolsSettings.port,
    workers=1,
    reload=True
  )