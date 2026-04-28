from app.extensions import db
from sqlalchemy.sql import func

class Product(db.Model):
    __tablename__ = "Products"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float)
    brand = db.Column(db.String)
    image = db.Column(db.String)
    trend = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # FK
    category_id = db.Column(db.String, db.ForeignKey("Categories.id"))

    # relación hacia Category
    category = db.relationship("Category", back_populates="products")