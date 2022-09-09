from typing import Optional

from kombu import Queue
from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    UVICORN_PORT: int = 8000
    LOGGER_PATH: str = "/var/log/syncbyte"
    CACHE_VOLUME: str = "/var/run/syncbyte"
    HOST_PATH: str = "/var/run/syncbyte"
    DATABASE_URI: PostgresDsn
    REDIS_URI: Optional[RedisDsn]
    RABBIT_MQ_URI: Optional[str]
    IS_LOCAL_DUMP: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()


class CeleryConfig:
    broker_url = settings.RABBIT_MQ_URI or settings.REDIS_URI
    result_expires = 60 * 60 * 24
    worker_hijack_root_logger = False

    task_queues = (
        Queue("remote_q", routing_key="remote_backup_async"),
        Queue("default", routing_key="default"),
    )

    task_routes = {
        "app.celery.remote_backup_async": {"queue": "remote_q", "routing_key": "remote_backup_async"},
        "app.celery.complete_backup_async": {"queue": "default", "routing_key": "default"},
    }
