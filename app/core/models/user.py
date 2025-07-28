from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Boolean, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base


if TYPE_CHECKING:
    from core.models import Profile
    from .post import Post


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str]
    password: Mapped[bytes]
    email: Mapped[str | None] = None
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    profile: Mapped['Profile'] = relationship(
        back_populates='user',
    )
    posts: Mapped['Post'] = relationship(
        back_populates='user'
    )
