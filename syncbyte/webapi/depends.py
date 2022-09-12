from syncbyte.db import get_session


def get_db():
    try:
        db = get_session()
        yield db
    finally:
        db.close()
