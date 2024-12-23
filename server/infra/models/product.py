

from typing import Literal, Optional
from pydantic import BaseModel


class Product(BaseModel):
    article: int
    nameproduct: str
    description: Optional[str]
    volume: int
    size: str 
    country: str
    age: str
    price: float
    quantitystock: int
    season: Literal['winter', 'summer', 'autom', 'spring', 'universal']
    idcategory: int