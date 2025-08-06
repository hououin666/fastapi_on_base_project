from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Boolean, String, LargeBinary, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from core.models.base import Base


if TYPE_CHECKING:
    from core.models import Profile
    from .post import Post
    from core.models import Role


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
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('false'), nullable=False,)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), default=1, server_default=text('1'))
    role: Mapped['Role'] = relationship(back_populates='users')