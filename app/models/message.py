from app.extensions import db
from sqlalchemy.sql import func

class Message(db.Model):
    __tablename__ = "Messages"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    lastname = db.Column(db.String)
    subject = db.Column(db.String)
    email = db.Column(db.String)
    message = db.Column(db.String)
    opened = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())