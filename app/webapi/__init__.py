from fastapi import FastAPI, APIRouter

from app.celery import test_async
from .api import router as api_router

app = FastAPI(title="syncbyte")
router = APIRouter()

router.include_router(api_router)
app.include_router(router)


@app.get("/ping")
def ping():
    return {"result": "pong"}
