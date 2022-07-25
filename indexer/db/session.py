from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.settings import config

SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    # required for sqlite
    #connect_args={"check_same_thread": False},
    echo=True,
    #extend_existing=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)
