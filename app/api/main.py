from fastapi import FastAPI
from app.api.endpoints import filters, location

app = FastAPI(title="Real Estate API")
app.include_router(filters.router)
app.include_router(location.router)
