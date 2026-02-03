from fastapi import FastAPI
from backend import models
from backend.models import db as engine 
from backend.routes import router
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.routes import router

app.include_router(router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)