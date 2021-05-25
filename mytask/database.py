import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_path = os.path.join(Path.home(), 'mytask.db')
engine = create_engine(f'sqlite:///{db_path}',connect_args={
        "check_same_thread": False
    }
)

Session = sessionmaker(bind=engine)

Base = declarative_base()