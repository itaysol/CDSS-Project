from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(title="CDSS Temporal DB API")
app.include_router(api_router)