from pydantic import BaseModel


class Post(BaseModel):
    title: str
    body: str


class PostUser(Post):
    id: int
    user_id: int