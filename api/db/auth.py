from datetime import datetime, timedelta
from typing import Generator, Optional
from typing import MutableMapping, List, Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from starlette import status
from api.core.settings import SECRET_KEY, ALGORITHM
from api.db.crud import crud_token
from api.db.models.token import Token
from api.db.models.user import User
from api.db.session import SessionLocal

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
        data: dict,
        email: str,
        token_type: str,
        db: Session,
        sub: str,
        expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.utcnow()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    result = db.query(Token).filter(Token.submitter_id == sub).first()
    if result is not None:
        crud_token.token.remove(db=db, id=result.id)
    payload = {}

    payload.update({"exp": expire.timestamp()})
    payload.update({"token_type": "type"})
    payload.update({"sub": email})
    payload.update({"iat": datetime.utcnow().timestamp()})
    payload.update({"submitter_id": sub})
    payload.update({"access_token": encoded_jwt})
    payload.update({"token_type": token_type})

    crud_token.token.create(db=db, obj_in=payload)

    return encoded_jwt
