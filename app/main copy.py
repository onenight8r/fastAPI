from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    likes:Optional[int]=0
    public: bool =True

my_posts = [{"tilte":"This is the first title of the profile","content":"this content isabout life","id":1},
            {"tilte":"This is the first title of the 2profile","content":"this content isabout 2life","id":2},
            {"tilte":"This is the first title of the 3profile","content":"this content isabout 3life","id":3},
            {"tilte":"This is the first title of the 4profile","content":"this content isabout 4life","id":4},
            {"tilte":"This is the first title of the 5profile","content":"this content isabout 5life","id":5}]

#GET ALL THE POST IN THE SYSTEM
@app.get("/posts")
def get_posts():
    return {"posts":my_posts}

#GET THE POST FROM A SPECIFC ID
def get_id(id):
    for p in my_posts:
        if p["id"]==id:
            return p
        

@app.get("/posts/{id}")
def get_post_id(id:int):
    post_result=get_id(id)
    if post_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post is not there")
        #The detail
    
    return {"Here is the post":post_result}


#CREATE A POST
@app.post("/posts",status_code = status.HTTP_201_CREATED)
def add_post(post:Post):
    post_dict=post.dict()
    post_dict["id"]=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"Poste Updated":post_dict}

#UPDATE A POST
def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"]==id:
            return i
    return None

@app.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int,post:Post):
    index=find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post is not present")
    
    post_dict = post.dict()
    my_posts[index]=post_dict
    return {"update post":"the post with the id has been updated"}


#DELETE A POST
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    index=find_index(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the record is absent")
    
    my_posts.pop(index)
    return {'message':"the mnessage is deleted"}
















# @app.get("/")
# def test():
#     return{"messgae":"this test is working"}