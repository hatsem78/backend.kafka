from sqlalchemy import Column, String, Integer

from db.base_class import Base


class Auto(Base):

    __tablename__ = "autos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=True)
    make = Column(String(256), nullable=True)
    model = Column(String(256), nullable=True)
    category = Column(String(256), nullable=True)

