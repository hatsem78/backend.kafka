from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from db.crud.base import CRUDBase
from db.models.token import Token
from db.models.user import User
from db.schemas import UserCreate
from db.schemas.token import TokenCreate, TokenUpdate
from db.schemas.user import UserUpdate


class CRUDToken(CRUDBase[Token, TokenCreate, TokenUpdate]):
   ...


token = CRUDToken(Token)
