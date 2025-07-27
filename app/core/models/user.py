from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base


if TYPE_CHECKING:
    from core.models import Profile


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str | None] = None
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    profile: Mapped['Profile'] = relationship(
        back_populates='user'
    )
