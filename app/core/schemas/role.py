from pydantic import BaseModel


class Role(BaseModel):
    name: str


class RoleCreate(Role):
    pass


class RoleDB(Role):
    id: int