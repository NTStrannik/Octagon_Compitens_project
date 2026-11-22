from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.db.db import get_db


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# Получить список категорий
@router.get("/", response_model=list[schemas.CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


# Получить категорию по ID
@router.get("/{category_id}", response_model=schemas.CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    return category


# Создать категорию
@router.post(
    "/",
    response_model=schemas.CategoryOut,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    data: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    return crud.create_category(db, data.title)


# Обновить категорию
@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(
    category_id: int,
    data: schemas.CategoryUpdate,
    db: Session = Depends(get_db)
):
    category = crud.update_category(db, category_id, data.title)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    return category


# Удалить категорию
@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    if category.books:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Нельзя удалить категорию, к которой привязаны книги"
        )

    crud.delete_category(db, category_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)