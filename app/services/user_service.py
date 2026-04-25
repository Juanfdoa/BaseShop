import uuid
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

def get_users():
    return User.query.all()

def get_user_by_id(id):
    return User.query.get(id)

def add_user(name, lastname, email, password, image):
    hashed_password = generate_password_hash(password)

    user = User(
        id= str(uuid.uuid4()),
        name=name,
        lastname=lastname,
        email=email,
        password=hashed_password,
        image=image
    )

    db.session.add(user)
    db.session.commit()

    return user

def put_user(id, name, lastname, email, image, password=None):
    user = User.query.get(id)

    if not user:
        return None

    user.name = name
    user.lastname = lastname
    user.email = email
    user.image = image

    if password:
        hashed_password = generate_password_hash(password)
        user.password = hashed_password 

    db.session.commit()

    return user

def delete_user(id):
    user = User.query.get(id)

    if not user:
        return False

    db.session.delete(user)
    db.session.commit()

    return True
    