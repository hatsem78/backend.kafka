import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, StrictFloat
from datetime import datetime, timedelta
from core.settings import config
from db.models.core import CoreModel


class JWTMetaBase(CoreModel):
    iss: Optional[str] = "phresh.io"
    aud: Optional[str] = config.JWT_AUDIENCE
    iat: Optional[StrictFloat] = datetime.timestamp(datetime.utcnow())
    exp: Optional[StrictFloat] = datetime.timestamp(datetime.utcnow() +
                                                    timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))


# Properties to receive via API on creation
class TokenCreate(JWTMetaBase):
    iss: Optional[str] = "phresh.io"
    aud: Optional[str] = config.JWT_AUDIENCE
    iat: Optional[StrictFloat] = datetime.timestamp(datetime.utcnow())
    exp: Optional[StrictFloat] = datetime.timestamp(
    datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))


# Properties to receive via API on update
class TokenUpdate(JWTMetaBase):
    ...


class JWTMeta(CoreModel):
    iss: str = "phresh.io"
    aud: str = config.JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))


class JWTCreds(CoreModel):
    """How we'll identify users"""

    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """

    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class RefreshToken(BaseModel):
    id: uuid.UUID
    user_id: str
    validity_timestamp: float