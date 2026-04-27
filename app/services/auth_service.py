from flask_login import login_user
from werkzeug.security import check_password_hash
from app.models.user import User

def authenticate(email, password):
    if not email or not password:
        return {"success": False,"message": "Campos obligatorios"}

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"success": False,"message": "Usuario no existe"}

    if not check_password_hash(user.password, password):
        return {"success": False,"message": "Contraseña incorrecta"}

    login_user(user)
    return {
        "success": True,
        "id": user.id,
        "user": f'{user.name} {user.lastname}',  
        "image": user.image
    }