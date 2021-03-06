from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm.session import Session
from app.models import User
from app.schema.user_schema import TokenData
from app.database import get_db
from app.config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    data_copy = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expire})

    res = jwt.encode(data_copy, SECRET_KEY, ALGORITHM)
    return res


def verify_access_token(token: str, credentials_exception):
    try:
        res = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = res.get("id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()

    return user.id
