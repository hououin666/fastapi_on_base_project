from pydantic import EmailStr
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str | None] = None
    active: Mapped[bool] = mapped_column(Boolean, default=True)
