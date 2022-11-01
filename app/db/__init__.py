from . import models
from .session import get_session, set_uri, create_all


async def init(uri):
    set_uri(uri)
    await create_all()
