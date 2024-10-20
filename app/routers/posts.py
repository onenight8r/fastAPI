from fastapi import FastAPI, HTTPException, status,Depends,APIRouter
from fastapi.params import Body
from typing import List
from random import randrange
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session 
from .. import models,schemas,utilis
from ..database import get_db

router=APIRouter(
    prefix="/posts",tags=["Posts"]
)

@router.get("/",response_model=List[schemas.Post])
def test_post(db:Session = Depends(get_db)):
    posts=db.query(models.Post).all() #query is sending the sql data query-.all() is giving the the result for retirnving the result
    return{"data":posts}
#psycopg2 
# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     post=cursor.fetchall()
#     return {"data":post}

#CREATE A POST
#Alchemy
@router.post("/",status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.Post, db:Session=Depends(get_db)):
    
    #new_post=models.Post(title=post.title, content=post.content,published=post.published)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#retrieve the new data and add it int the newpost
    return{"data":new_post}

# @app.post("/posts",status_code = status.HTTP_201_CREATED)
# def add_post(post:Post):
#     cursor.execute("INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING *",
#                    (post.title,post.content,post.published))
#     post_made=cursor.fetchone()
#     #sql injection migth be possible if instead of %s we use directly there
#     conn.commit()

    
#     return {"Poste Updated":post_made}
#GET POST FROM ID  
@router.get("/{id}",status_code=status.HTTP_200_OK)
def get_posts(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with {id} is not present")

    return{"post details":post}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no such data{id}")
    
    post.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}")
def update_posts(id:int,update_post:schemas.Post,db:Session=Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post =post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "this is the updated method")
    post_query.update(update_post.dict(),synchronize_session=False)
    db.commit()

    return {"data": update_post}

@router.put("/new/{id}",status_code=status.HTTP_202_ACCEPTED)
def newupost(id:int,newpost:schemas.Post,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id)
    postdata=post.first()
    if postdata is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the data is not present")
    
    post.update(newpost.dict(),synchronize_session=False)
    db.commit()
    return {"data":newpost}