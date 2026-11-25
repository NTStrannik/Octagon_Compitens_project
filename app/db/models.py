
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.db.db import Base
# Таблица категорий
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    books = relationship(
        "Book",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
# Таблица книг
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    url = Column(String(500))

    category_id = Column(
        Integer,
        ForeignKey(
            "categories.id",
            ondelete="CASCADE",
            name="fk_books_category_id"
        ),
        nullable=False
    )

    category = relationship("Category", back_populates="books")