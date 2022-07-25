from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from api.db.base_class import Base


class User(Base):

    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    tokens = relationship(
        "Token",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )

    # New addition
    hashed_password = Column(String, nullable=False)
