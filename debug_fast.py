import sys
from unittest.mock import MagicMock

# Mock ml_engine before importing api
sys.modules["app.ml_engine"] = MagicMock()
sys.modules["app.ml_engine"].model_instance = MagicMock()

from fastapi import FastAPI
from app.api import router

app = FastAPI()
app.include_router(router)

print("Registered Routes:")
for route in app.routes:
    print(f"{route.path} [{route.methods}]")
