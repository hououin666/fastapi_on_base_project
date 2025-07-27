from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.models import Base


class Profile(Base):
    __tablename__ = 'profiles'

    first_name: Mapped[str]
    last_name: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
    )
    # user: Mapped['User'] = relationship(
    #
    # )