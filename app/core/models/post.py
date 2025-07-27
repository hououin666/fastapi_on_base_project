from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .user import User


class Post(Base):
    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(String(40))
    body: Mapped[str] = mapped_column(String(300))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    user: Mapped['User'] = relationship(
        back_populates= 'posts'
    )

