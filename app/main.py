from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 


while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
                                password='123qwe',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('databse connection succesful')
        break

    except Exception as error:
        print("databse connection failed")
        print("error",error)
        time.sleep(20)


app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True


#GET ALL THE POST IN THE SYSTEM
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    post=cursor.fetchall()
    return {"data":post}

#CREATE A POST
@app.post("/posts",status_code = status.HTTP_201_CREATED)
def add_post(post:Post):
    cursor.execute("INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING *",
                   (post.title,post.content,post.published))
    post_made=cursor.fetchone()
    #sql injection migth be possible if instead of %s we use directly there
    conn.commit()

    
    return {"Poste Updated":post_made}

#CREATE 
@app.get("/posts/{id}")
def get_post_id(id:int):
    cursor.execute("SELECT * FROM posts WHERE id=%s",str(id))
    post_result=cursor.fetchone()
    if post_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post is not there")
        #The detail
    
    return {"Here is the post":post_result}

#DELETE AN ID FROM THE TABLE
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *",(id,))
    deleted_post = cursor.fetchone()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post is empty")
    conn.commit()
    return{"message":deleted_post}

#UPDATE A POST
@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def updated_post(id:int, post:Post):
    cursor.execute("UPDATE posts SET title=%s, content = %s, published=%s WHERE id=%s RETURNING *",
                   (post.title,post.content,post.published,id))
    update_post=cursor.fetchone()
    conn.commit()
    if update_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Wrong id")
    return{"post updated":update_post}
    

#GET THE POST FROM A SPECIFC ID
# def get_id(id):
#     for p in my_posts:
#         if p["id"]==id:
#             return p
        




#

#UPDATE A POST
# def find_index(id):
#     for i, p in enumerate(my_posts):
#         if p["id"]==id:
#             return i
#     return None

# @app.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
# def update_post(id:int,post:Post):
#     index=find_index(id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post is not present")
    
#     post_dict = post.dict()
#     my_posts[index]=post_dict
#     return {"update post":"the post with the id has been updated"}


# #DELETE A POST
# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_posts(id:int):
#     index=find_index(id)

#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the record is absent")
    
#     my_posts.pop(index)
#     return {'message':"the mnessage is deleted"}
















# @app.get("/")
# def test():
#     return{"messgae":"this test is working"}