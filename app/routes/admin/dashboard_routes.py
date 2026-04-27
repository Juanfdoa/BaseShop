from flask_login import login_required
from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from app.services.helper_service import get_dashboard_stats

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('/admin/dashboard')
@login_required
def dashboard():
    try:
        if "user" not in session:
            return redirect(url_for("auth/login"))

        stats = get_dashboard_stats()
        return render_template('admin/dashboard.html', user=session['user'], stats=stats)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500