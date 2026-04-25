from app.extensions import db

class Category(db.Model):
    __tablename__ = "Categories"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)
    count = db.Column(db.Integer)

    # relations
    products = db.relationship("Product", back_populates="category")