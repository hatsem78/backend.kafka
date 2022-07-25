from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from api.db.crud.base import CRUDBase
from api.db.models.token import Token
from api.db.models.user import User
from api.db.schemas import UserCreate
from api.db.schemas.token import TokenCreate, TokenUpdate
from api.db.schemas.user import UserUpdate


class CRUDToken(CRUDBase[Token, TokenCreate, TokenUpdate]):
   ...


token = CRUDToken(Token)
