from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
import schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model= schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Depends() without an argument tells FastAPI "Use the type hint OAuth2PasswordRequestForm to figure out what dependency to inject"
    # In this case, FastAPI parses the request form data, creates an instance of OAuth2PasswordRequestForm and assigns it to user_creds
    # OAuth2 spec expects the header fields as 'username' and 'password'
    existing_user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_creds.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    # Create JWT token, input will be the payload you desire to pass. Here we are passing user ID, and also adding the creation time of token internally.
    access_token = oauth2.create_access_token(data={"user_id" : existing_user.id})
    return {"access_token": access_token, "token_type": "bearer"}