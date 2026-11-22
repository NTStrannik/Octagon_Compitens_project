from app.db.db import SessionLocal
from app.db.crud import get_categories

# Открываем сессию
db = SessionLocal()

try:
    # Получаем категории
    categories = get_categories(db)

    # Выводим категории и книги
    for category in categories:
        print(f"\nКатегория: {category.title}")

        for book in category.books:
            print(f"  Название: {book.title}")
            print(f"  Описание: {book.description}")
            print(f"  Цена: {book.price} руб.")
            print(f"  Ссылка: {book.url}")
            print()

finally:
    db.close()