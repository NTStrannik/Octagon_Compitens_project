from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


# ---------- CATEGORIES ----------

class CategoryBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- BOOKS ----------

class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    price: Decimal = Field(ge=0)
    url: str | None = None
    category_id: int = Field(gt=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookOut(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)