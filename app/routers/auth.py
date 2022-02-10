from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2


router = APIRouter(
    tags=["Authentication"]
)


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # The Oauth2form will return username and password
    # Our username here is email
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN_NOT_FOUND, detail= f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN_NOT_FOUND, details=f"Invalid Credentials")

    # create  a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})   # passing user id to th payload
    # return token
    return {"access_token": access_token, "token_type": "bearer"}
