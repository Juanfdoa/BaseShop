import uuid
import bleach
from datetime import datetime
from app import db
from sqlalchemy import func
from app.models.product import Product
from app.models.category import Category
from app.services.external_services import upload_image

ALLOWED_TAGS = [
    'b', 'br'
]

def clean_description(html):
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        strip=True
    )

def get_products(search=None, category=Category, page=1, per_page=8):
    query = Product.query

    if search:
        search = search.lower()
        query = query.filter(
            func.lower(Product.name).like(f"%{search}%")
        )

    if category:
        category = category.lower()
        query = query.join(Category).filter(
            func.lower(Category.name).like(f"%{category}%")
        )

    query = query.order_by(Product.updated_at.desc())
    return query.paginate(page=page, per_page=per_page, error_out=False)

def get_product_by_id(id):
    return Product.query.filter_by(id=id).first()

def get_trend_products():
    return  Product.query.filter_by(trend=True).order_by(Product.updated_at.desc()).all()

def add_product(category_id, name, description, price, brand, image, trend =False):

    image_url = upload_image(image)

    product = Product(
        id= str(uuid.uuid4()),
        category_id = category_id,
        name = name,
        description = description,
        price = price,
        brand = brand,
        image = image_url,
        trend = trend,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.session.add(product)

    category = Category.query.get(category_id)
    if category:
        category.count = category.count + 1

    db.session.commit()

    return product

def put_product(id, category_id, name, description, price, brand, image, current_image, trend=False):
    product = Product.query.get(id)

    if not product:
        return None
    
    image_url = None
    if image:
        image_url = upload_image(image)
    else:
        image_url = current_image

    product.category_id = category_id
    product.name = name
    product.description = description
    product.price = price
    product.brand = brand
    product.image = image_url
    product.trend = trend
    product.created_at = product.created_at
    product.updated_at = datetime.now()
    
    db.session.commit()

    return product

def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return False
    
    category = Category.query.get(product.category_id)
    if category:
        category.count = category.count - 1

    db.session.delete(product)

    db.session.commit()

    return True



