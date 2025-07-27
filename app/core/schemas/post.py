from pydantic import BaseModel


class Post(BaseModel):
    title: str
    body: str


class PostUser(Post):
    user_id: int