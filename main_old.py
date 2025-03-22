

### APPROACH: USING PSYCOPG2 NATIVE DRIVER TO EXECUTE SQL COMMANDS


from email.policy import HTTP
import stat, time, os, sys, signal
import psycopg2
from psycopg2.extras import RealDictCursor # To get the data in dictionary format
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    # Code will not proceed further if there is any error
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres',password='iEnable@123', cursor_factory=RealDictCursor)
        #RealDictCursor returns the columns as a Dict with key as column name. Default behaviour is just to return the column values without the names of the col
        cursor = connection.cursor()
        print(f"*******Successfully connected to the database*******")
        break

    except Exception as e:
        time.sleep(5)
        print(f"Could not connect. Error: {e}")
        

@app.get("/posts")
async def root():
    cursor.execute("SELECT * FROM posts") #Executes the SQL query on the DB but does not return results in memory/to your python program
    posts = cursor.fetchall() #Fetches as many rows as needed into memory. 
    # print(posts)
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id= %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        # Alternate ways
        # response.status_code = 404 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data":"No such post found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such post found")
    print(post)
    return {"data":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id= %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such post found")
    connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
def update_post(id: int, new_post: Post):
    cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *", (new_post.title, new_post.content, new_post.published, str(id)))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such post found")
    connection.commit()
    return {"data":updated_post}