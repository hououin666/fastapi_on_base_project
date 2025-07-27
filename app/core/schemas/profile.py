from pydantic import BaseModel



class ProfileSchema(BaseModel):
    first_name: str
    last_name: str


class ProfileUser(ProfileSchema):
    user_id: int