from fastapi import FastAPI
from app.api.v1.places import router as places_router
from app.db.session import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(places_router, prefix="/api/v1")
