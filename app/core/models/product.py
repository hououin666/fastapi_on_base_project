from sqlalchemy.orm import Mapped

from core.models import Base


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str]
    count: Mapped[int]
