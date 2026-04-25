from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.services.category_service import get_categories, get_category_by_id, add_category, put_category, delete_category

admin_category_bp = Blueprint('admin_category', __name__)

@admin_category_bp.route('/admin/categories')
@login_required
def categories():
    categories = get_categories()
    return render_template('admin/categories.html', categories=categories)

@admin_category_bp.route("/admin/categories/form")
@login_required
def category_form():
    return render_template("components/forms/category_form.html")

@admin_category_bp.route("/admin/categories/create", methods=["POST"])
@login_required
def create_category():
    name = request.form.get("name")
    icon = request.form.get("icon")

    new_category = add_category(name, icon)
    html = render_template("components/accordion.html", item=new_category)

    return jsonify({
        "success": True,
        "html": html
    })

@admin_category_bp.route("/admin/categories/form", defaults={"id": None})
@admin_category_bp.route("/admin/categories/form/<id>")
@login_required
def category_form_update(id):

    print('ENTRO AL PUT')
    print(id)
    category = None

    if id:
        category = get_category_by_id(id)

    return render_template("components/forms/category_form.html", category=category)

@admin_category_bp.route("/admin/categories/update/<id>", methods=["POST"])
@login_required
def update_category(id):
    name = request.form.get("name")
    icon = request.form.get("icon")

    put_category(id,name,icon)

    return jsonify({
        "success": True,
        "message": "Categoria actualizada"
    })

@admin_category_bp.route("/admin/categories/delete/<id>", methods=["POST"])
@login_required
def delete_category_route(id):
    success = delete_category(id)
    if not success:
            return jsonify({
                "success": False,
                "message": "Categoria no encontrada"
            })
    return jsonify({
        "success": True,
        "message": "Categoria eliminada"
    })