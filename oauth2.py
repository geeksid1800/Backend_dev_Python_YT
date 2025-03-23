from typing import Any
from fastapi import Depends, status, HTTPException
import jwt
from datetime import datetime, timedelta,timezone
from fastapi.security import OAuth2PasswordBearer
import schemas
from database import get_db
from sqlalchemy.orm import Session
import models
from config import settings

SECRET_KEY = settings.JWT_secret_key
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login') #The path of your login endpoint (i.e. '/login' for us)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #add the expiration time to the payload, so we can check it.
    to_encode.update({"expiration_time": expire.isoformat()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception) -> int | None: 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        expiration_time = payload.get("expiration_time")
        if user_id is None:
            raise credentials_exception
        if expiration_time < datetime.now().isoformat():
            raise jwt.ExpiredSignatureError("Signature has expired")
        return payload
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User | Any:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception) #If the token is valid, the function will return the token's payload
    current_user: schemas.UserResponse = db.query(models.User).filter(models.User.id == token_data.get("user_id")).first()
    return current_user