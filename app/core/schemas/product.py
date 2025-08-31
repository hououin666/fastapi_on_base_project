from pydantic import BaseModel


class Product(BaseModel):
    name: str
    count: int

class ProductCreate(Product):
    pass


class ProductShow(Product):
    id: int