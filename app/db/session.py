from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from .models import Base

URI = None

_ENGINE = None
_MAKER = None


def set_uri(uri):
    global URI

    URI = uri


def get_engine(echo=False):
    global _ENGINE

    if _ENGINE is None:
        _ENGINE = create_async_engine(URI, echo=echo)

    return _ENGINE


async def create_all():
    engine = get_engine()
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_session(expire_on_commit=False) -> Session:
    global _MAKER

    if _MAKER is None:
        engine = get_engine()
        _MAKER = sessionmaker(
            bind=engine, expire_on_commit=expire_on_commit, class_=AsyncSession
        )

    return _MAKER()
