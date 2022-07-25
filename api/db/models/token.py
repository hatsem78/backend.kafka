from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from api.db.base_class import Base


class Token(Base):

    __tablename__ = "tokens"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    token_type = Column(String(256), nullable=True)
    access_token = Column(String(256), nullable=True)
    sub = Column(String(256), nullable=True)
    iat = Column(Float, nullable=True)
    exp = Column(Float, nullable=True)
    submitter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    submitter = relationship("User", back_populates="tokens")

