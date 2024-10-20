from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..database import get_db
from .. import schemas,models,utilis
from . import oauth2


router=APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.email==user_credentials.username).first()
    #using oauth2passowrd allow us to acces useranme and passowrd, dictionary, thats why
    #user_crednital.email is not gonna work = user_credential.username
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no user from this email")
    if not utilis.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}