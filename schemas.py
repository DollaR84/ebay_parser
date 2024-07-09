from pydantic import BaseModel


class Product(BaseModel):
    name: str
    image: str
    url: str

    currency: str
    price: float

    seller: str
    delivery: str

    model: str | None = None
    brand: str | None = None
