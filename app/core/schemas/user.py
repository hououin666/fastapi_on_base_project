from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    active: bool = True


class UserCreate(UserSchema):
    pass

class UserRead(UserSchema):
    pass
