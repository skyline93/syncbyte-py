from fastapi import FastAPI, APIRouter

from syncbyte.celery import test_async
from .api import router as api_router

app = FastAPI(title="syncbyte")
router = APIRouter()

router.include_router(api_router)
app.include_router(router)


@app.get("/ping")
def ping():
    return {"result": "pong"}


@app.get("/ping/celery")
def ping_celery():
    task = test_async.delay(0)
    return {
        "result": {
            "task_id": f"{task.id}"
        }
    }
