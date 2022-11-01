class Entity:
    def __init__(self, id, **kwargs):
        self.id = id

    def __await__(self):
        async def closure():
            await self._load_from_db()
            return self

        return closure().__await__()

    async def _load_from_db(self):
        pass
