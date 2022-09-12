from datetime import datetime

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from syncbyte.config import settings

DATABASE_URI = settings.DATABASE_URI

_ENGINE = None
_MAKER = None


def get_engine():
    global _ENGINE

    if _ENGINE is None:
        engine_args = {
            "echo": False,
            "pool_recycle": 3600,
        }

        _ENGINE = sqlalchemy.create_engine(DATABASE_URI, **engine_args)

        _ENGINE.connect()

    return _ENGINE


def get_session(expire_on_commit=False):
    global _MAKER

    if _MAKER is None:
        engine = get_engine()
        _MAKER = sqlalchemy.orm.sessionmaker(bind=engine, expire_on_commit=expire_on_commit)

    return _MAKER()


@as_declarative()
class ModelBase:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)


class Resource(ModelBase):
    __tablename__ = "resource"

    name = Column(String(60))
    db_type = Column(String(20))
    db_version = Column(String(60))
    host = Column(String(60))
    port = Column(Integer)
    user = Column(String(60))
    password = Column(String(500))
    dbname = Column(String(100))
    args = Column(String(600))


class S3(ModelBase):
    __tablename__ = "s3"

    endpoint = Column(String(60))
    access_key = Column(String(200))
    secret_key = Column(String(200))
    bucket_name = Column(String(120))
    type = Column(String(30))


class BackupJob(ModelBase):
    __tablename__ = "backup_job"

    start_time = Column(DateTime)
    end_time = Column(DateTime)
    size = Column(Integer)
    is_valid= Column(Boolean, default=False)
    status = Column(String(20))
    resource_id = Column(Integer)
    storage_id = Column(Integer)
    dataset_name = Column(String(200))
