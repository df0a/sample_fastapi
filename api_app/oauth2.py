from fastapi import Depends , HTTPException , status 
from jose import jwt , JWTError
from datetime import datetime , timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'e1acf9ce82a01fd53dd523d1557c84ce5913bb75d93e33ba629e1960b04794c2'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str , credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise JWTError("Invalid token")
        token_data = schemas.TokenData(user_id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    payload = verify_access_token(token, credentials_exception)
    return payload.user_id