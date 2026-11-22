from app.db.db import Base, engine, SessionLocal
from app.db.crud import (
    create_category,
    create_book,
    get_categories,
    get_books
)
from app.db import models


# Создаём таблицы
Base.metadata.create_all(bind=engine)


# Открываем сессию
db = SessionLocal()

try:
    # Создаём категории
    categories = {
        category.title: category
        for category in get_categories(db)
    }

    names = ["Художественная литература", "Научная литература"]

    for name in names:
        if name not in categories:
            categories[name] = create_category(db, name)

    # Добавляем книги
    books = [
        ("Мастер и Маргарита", "Роман Михаила Булгакова", 650,
         None, "Художественная литература"),

        ("Преступление и наказание", "Роман Фёдора Достоевского", 550,
         None, "Художественная литература"),

        ("Война и мир", "Роман Льва Толстого", 900,
         None, "Художественная литература"),

        ("Краткая история времени", "Книга Стивена Хокинга", 750,
         None, "Научная литература"),

        ("Космос", "Научно-популярная книга об устройстве Вселенной", 600,
         None, "Научная литература"),

        ("Происхождение видов", "Труд Чарльза Дарвина", 800,
         None, "Научная литература")
    ]

    # Проверяем, какие книги уже есть
    existing = {
        (book.title, book.category_id)
        for book in get_books(db)
    }

    for title, desc, price, url, cat_name in books:
        category = categories[cat_name]

        if (title, category.id) not in existing:
            create_book(
                db,
                title,
                desc,
                price,
                url,
                category.id
            )

    print("База данных успешно заполнена!")

finally:
    db.close()