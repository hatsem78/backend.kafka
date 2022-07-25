from fastapi import HTTPException
from jose.exceptions import JWTClaimsError
from db.models.user import User
from jose import jwt, JWTError, ExpiredSignatureError
from starlette import status
from core.settings import SECRET_KEY, ALGORITHM
from db.session import SessionLocal


def valid_token(token):

    db = SessionLocal()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise auth_token_error("Could not validate credentials")
    except ExpiredSignatureError:
        raise auth_token_error("Signature has expired")
    except JWTClaimsError as error:
        raise auth_token_error(str(error))
    except JWTError:
        raise auth_token_error("Invalid signature")

    return token


def auth_token_error(msg):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        headers={"WWW-Authenticate": "Bearer"},
    )

    return credentials_exception
