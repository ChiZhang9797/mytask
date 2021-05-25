from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from .database import Base

class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_date = Column(DateTime, default=datetime.now())

