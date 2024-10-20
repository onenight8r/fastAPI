
from fastapi import FastAPI, HTTPException, status,Depends,APIRouter
from fastapi.params import Body
from typing import Optional
from random import randrange
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session 
from .. import models,schemas,utilis
from ..database import get_db

router=APIRouter(
    prefix="/users",tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    #has the password
    user.password=utilis.hash_password(user.password)
   
    new_user=models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_id_users(id:int,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the data was not found")
    return user

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)#if the value is not default it nees to be passed
def update_user(id:int,userdetails:schemas.Users,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id)
    uservalue=user.first()
    if uservalue == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    user.update(userdetails.dict(),synchronize_session=False)
    db.commit
    return{"detailes":uservalue}
