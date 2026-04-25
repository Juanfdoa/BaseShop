import uuid
from app import db
from app.models.category import Category


def get_categories():
    return Category.query.all()

def get_category_by_id(id):
    return Category.query.get(id)

def add_category(name,icon):
    category = Category(
        id= str(uuid.uuid4()),
        name=name,
        icon=icon,
        count=0
    )

    db.session.add(category)
    db.session.commit()

    return category

def put_category(id, name, icon):
    category = Category.query.get(id)

    if not category:
        return None

    category.name = name
    category.icon = icon

    db.session.commit()

    return category

def delete_category(id):
    category = Category.query.get(id)

    if not category:
        return False

    db.session.delete(category)
    db.session.commit()

    return True