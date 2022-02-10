from typing import Optional

from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', port=5433, user='postgres', password='kehinde',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successfull.......")
        break
    except Exception as error:
        print("Connection to Database failed")
        print("Error: ", error)
        time.sleep(2000)

my_posts = [
    {"title": "Title of post 1", "content": "content of post 1", "id": 1},
    {"title": "Title of post 2", "content": "content of post 2", "id": 2}
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():  # The Async is optional
    return {"message": "Welcome to My Api"}


@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


""""@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)- 1]
    return {"data": post}"""


@app.get("/posts/{id}")
def get_post(id: int):                # The int here is validating
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))  # The str here is passed to the query
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE from posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")

    return {'data': updated_post}