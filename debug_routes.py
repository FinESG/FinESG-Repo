from fastapi import FastAPI
from app.api import router
from app.schemas import ChatRequest

app = FastAPI()
app.include_router(router)

print("Registered Routes:")
for route in app.routes:
    print(f"{route.path} [{route.methods}]")

print("\nSchema ChatRequest fields:")
print(ChatRequest.model_fields.keys())
