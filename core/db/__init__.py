from pkg import rds
from . import models


async def init(uri):
    rds.set_uri(uri)
    await rds.create_all()
