from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.db.db import get_db


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# Получить список книг с возможностью фильтрации
@router.get("/", response_model=list[schemas.BookOut])
def read_books(
    category_id: int | None = None,
    db: Session = Depends(get_db)
):
    if category_id is not None:
        category = crud.get_category(db, category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )

    return crud.get_books(db, category_id)


# Получить книгу по ID
@router.get("/{book_id}", response_model=schemas.BookOut)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return book


# Создать книгу
@router.post(
    "/",
    response_model=schemas.BookOut,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    data: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    category = crud.get_category(db, data.category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    return crud.create_book(
        db,
        data.title,
        data.description,
        data.price,
        data.url,
        data.category_id
    )


# Обновить книгу
@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(
    book_id: int,
    data: schemas.BookUpdate,
    db: Session = Depends(get_db)
):
    book = crud.get_book(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    category = crud.get_category(db, data.category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    return crud.update_book(
        db,
        book_id,
        data.title,
        data.description,
        data.price,
        data.url,
        data.category_id
    )


# Удалить книгу
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    crud.delete_book(db, book_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)