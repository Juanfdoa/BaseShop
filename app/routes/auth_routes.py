from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from app.services.auth_service import authenticate

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            result = authenticate(email, password)

            if result["success"]:
                session["user"] = result["user"]
                session["image"] = result["image"]
                return redirect(url_for("admin_dashboard.dashboard"))
            else:
                flash(result["message"])
                return redirect(url_for("auth.login"))

        return render_template("admin/login.html")
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))