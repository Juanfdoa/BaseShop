from flask_login import login_required
from flask import Blueprint, render_template, request, jsonify
from app.services.category_service import get_categories
from app.services.product_service import get_products, get_product_by_id, add_product, put_product, delete_product

admin_product_bp = Blueprint('admin_product', __name__)

@admin_product_bp.route('/admin/products')
@login_required
def products():
    try:
        page = request.args.get("page", 1, type=int)
        search = request.args.get('search', None)

        result = get_products(
            search=search, category=None, page=page, per_page=9
        )
        return render_template('/admin/products.html', products=result.items, pagination=result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@admin_product_bp.route("/admin/products/form")
@login_required
def product_form():
    categories = get_categories()
    return render_template("components/forms/product_form.html", categories=categories)

@admin_product_bp.route("/admin/products/create", methods=["POST"])
@login_required
def create_product():
    try:
        category_id = request.form.get("category_id")
        name = request.form.get("name")
        description = request.form.get("description")
        price = int(float(request.form.get("price")))
        brand = request.form.get("brand")
        image = request.files.get("image")
        trend = request.form.get("trend") is not None 

        new_product = add_product(category_id, name, description, price, brand, image, trend)
        html = render_template("components/accordion.html", item=new_product)

        return jsonify({"success": True,"html": html}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@admin_product_bp.route("/admin/products/form", defaults={"id": None})
@admin_product_bp.route("/admin/products/form/<id>")
@login_required
def product_form_update(id):
    categories = get_categories()
    product = None

    if id:
        product = get_product_by_id(id)

    return render_template("components/forms/product_form.html", categories=categories, product=product)

@admin_product_bp.route("/admin/products/update/<id>", methods=["POST"])
@login_required
def update_product(id):
    try:
        category_id = request.form.get("category_id")
        name = request.form.get("name")
        description = request.form.get("description")
        price = int(float(request.form.get("price")))
        brand = request.form.get("brand")
        image = request.files.get("image")
        current_image = request.form.get("current_image")
        trend = request.form.get("trend") is not None 

        put_product(id, category_id, name,description, price, brand, image, current_image, trend)

        return jsonify({"success": True,"message": "Producto actualizado"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@admin_product_bp.route("/admin/products/delete/<id>", methods=["POST"])
@login_required
def delete_product_route(id):
    try:
        success = delete_product(id)
        if not success:
                return jsonify({"success": False,"message": "Producto no encontrado"})
        return jsonify({"success": True,"message": "Producto eliminado"}), 204
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500