import cloudinary
from flask_login import LoginManager
from flask import Flask
from app.extensions import db
from app.jinja.context_processor import inject_translations
from app.errors.handlers import register_error_handlers
from app.routes.store_routes import store_bp
from app.routes.auth_routes import auth_bp
from app.routes.admin.dashboard_routes import admin_dashboard_bp
from app.routes.admin.user_routes import admin_user_bp
from app.routes.admin.category_routes import admin_category_bp
from app.routes.admin.product_routes import admin_product_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    cloudinary.config(
        cloud_name=app.config["CLOUD_NAME"],
        api_key=app.config["API_KEY"],
        api_secret=app.config["API_SECRET"],
        secure=True
    )
    
    # Jinja
    app.context_processor(inject_translations)
    
    # Errors
    register_error_handlers(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader         
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(user_id)

    # Blueprints
    app.register_blueprint(store_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_user_bp)
    app.register_blueprint(admin_category_bp)
    app.register_blueprint(admin_product_bp)

    return app