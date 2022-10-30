from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, Boolean

Base = declarative_base()


class ModelBase:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted = Column(Boolean, default=False)
