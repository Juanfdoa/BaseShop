from flask import Blueprint, render_template, request, jsonify
from app.services.category_service import get_categories
from app.services.product_service import get_products, get_product_by_id, get_trend_products
from app.services.message_service import add_message

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def home():
    try:
        categories = get_categories()
        trend_products = get_trend_products()
        return render_template('store/home.html', categories=categories, featured=trend_products)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@store_bp.route('/products')
def products():
    try:
        page = request.args.get("page", 1, type=int)
        search = request.args.get('search', None)
        category = request.args.get('category', None)

        result = get_products(search=search, category=category, page=page)
        categories = get_categories()
        
        return render_template('store/products.html', products=result.items, categories=categories, pagination=result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@store_bp.route('/product/<product_id>')
def producto(product_id):
    product = get_product_by_id(product_id)

    if not product:
        return render_template('store/404.html'), 404

    return render_template('store/product_details.html', product=product)

@store_bp.route('/about_us')
def about_us():
    return render_template('store/about_us.html')

@store_bp.route('/contact')
def contact():
    return render_template('store/contact.html')

@store_bp.route("/contact", methods=["GET", "POST"])
def submit_contact():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            subject = request.form.get("subject")
            message = request.form.get("message")

            add_message(name, lastname, email, subject, message)

            return render_template("store/contact.html", success=True)

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    return render_template("store/contact.html")