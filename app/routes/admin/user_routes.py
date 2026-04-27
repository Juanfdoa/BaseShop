from flask_login import login_required
from flask import Blueprint, render_template, request, jsonify
from app.services.user_service import get_users, add_user, get_user_by_id, put_user, delete_user

admin_user_bp = Blueprint('admin_user', __name__)

@admin_user_bp.route('/admin/users')
@login_required
def users():
    try:
        users = get_users()
        return render_template('/admin/users.html', users=users)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@admin_user_bp.route("/admin/users/form")
@login_required
def user_form():
    return render_template("components/forms/user_form.html")

@admin_user_bp.route("/admin/users/create", methods=["POST"])
@login_required
def create_user():
    try:
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        image = request.form.get("image")

        new_user = add_user(name,lastname,email,password,image)
        html = render_template("components/accordion.html", item=new_user)

        return jsonify({"success": True,"html": html}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@admin_user_bp.route("/admin/users/form", defaults={"id": None})
@admin_user_bp.route("/admin/users/form/<id>")
@login_required
def user_form_update(id):
    try:
        user = None

        if id:
            user = get_user_by_id(id)

        return render_template("components/forms/user_form.html", user=user)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@admin_user_bp.route("/admin/users/update/<id>", methods=["POST"])
@login_required
def update_user(id):
    try:
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        image = request.form.get("image")

        put_user(id,name,lastname,email,image, password)

        return jsonify({"success": True,"message": "Usuario actualizado"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@admin_user_bp.route("/admin/users/delete/<id>", methods=["POST"])
@login_required
def delete_user_route(id):
    try:
        success = delete_user(id)
        if not success:
            return jsonify({"success": False, "message": "Usuario no encontrado"})
        
        return jsonify({"success": True, "message": "Usuario eliminado"}), 204
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
