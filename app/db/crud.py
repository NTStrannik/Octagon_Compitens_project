from app.db.models import Book, Category


# ---------- CATEGORIES ----------

# CREATE
def create_category(db, title):
    category = Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# READ
def get_categories(db):
    return db.query(Category).all()


def get_category(db, category_id):
    return db.get(Category, category_id)


# UPDATE
def update_category(db, category_id, title):
    category = get_category(db, category_id)

    if category is None:
        return None

    category.title = title
    db.commit()
    db.refresh(category)
    return category


# DELETE
def delete_category(db, category_id):
    category = get_category(db, category_id)

    if category is None:
        return False

    db.delete(category)
    db.commit()
    return True


# ---------- BOOKS ----------

# CREATE
def create_book(db, title, description, price, url, category_id):
    book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


# READ
def get_books(db, category_id=None):
    query = db.query(Book)

    if category_id is not None:
        query = query.filter(Book.category_id == category_id)

    return query.all()


def get_book(db, book_id):
    return db.get(Book, book_id)


# UPDATE
def update_book(db, book_id, title, description, price, url, category_id):
    book = get_book(db, book_id)

    if book is None:
        return None

    book.title = title
    book.description = description
    book.price = price
    book.url = url
    book.category_id = category_id

    db.commit()
    db.refresh(book)
    return book


# DELETE
def delete_book(db, book_id):
    book = get_book(db, book_id)

    if book is None:
        return False

    db.delete(book)
    db.commit()
    return True