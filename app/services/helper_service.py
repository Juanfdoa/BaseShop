from app.models.user import User
from app.models.category import Category
from app.models.product import Product

def get_dashboard_stats():
    users_count      = User.query.count()
    categories_count = Category.query.count()
    products_count   = Product.query.count()

    return {
        "users":      users_count,
        "categories": categories_count,
        "products":   products_count
    }