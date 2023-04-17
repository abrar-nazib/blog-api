from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()         # Create a FastAPI instance


class Post(BaseModel):  # Post extends basemodel
    title: str
    content: str
    published: bool = True  # setting up default value for the field
    rating: Optional[int] = None  # optional field but has to be an integer
    # have to import Optional from typing module to use this


my_posts = [{"title": "My first post", "content": "This is my first post", "published": True, "rating": 5, "id": 1},
            {"title": "My second post", "content": "This is my second post",
                "published": False, "rating": 4, "id": 2},
            {"title": "My third post", "content": "This is my third post",
                "published": True, "rating": 3, "id": 3}
            ]


@app.get("/")           # Create a route
async def root():
    return {"message": "Say hello to FastAPI"}


@app.get("/posts")
def get_posts():
    # automatic serialization of my_post to JSON is done by FastAPI
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}  # return the last post in the list


@app.get("/posts/{id}")
def get_post(id: int):
    # high quality code by copilot :3
    post = next((post for post in my_posts if post["id"] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}
# create some sample requests for /posts endpoint
# POST http://
# { "title": "My first post", "content": "This is my first post" }  # This will create a post with default value of published field
# { "title": "My second post", "content": "This is my second post", "published": false }  # This will create a post with published field set to false
# { "title": "My third post", "content": "This is my third post", "published": true, "rating": 5 }  # This will create a post with published field set to true and rating field set to 5


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = next((post for post in my_posts if post["id"] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # Response is used to return a response without any data


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):

    # find the post index with the given id in the list
    post_index = next((index for (index, post) in enumerate(
        my_posts) if post["id"] == id), None)
    if not post_index:  # if post not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")  # raise an exception 404 not found
    post_dict = post.dict()  # convert the post object to a dictionary
    post_dict["id"] = id  # add the id to the dictionary
    my_posts[post_index] = post_dict  # update the post in the list
    # return the updated post
    return {"data": post_dict}
