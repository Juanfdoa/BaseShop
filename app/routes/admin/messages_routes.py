from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.services.message_service import get_messages, put_message_status

admin_messages_bp = Blueprint('admin_messages', __name__)

@admin_messages_bp.route('/admin/messages')
@login_required
def messages():
    try:
        messages = get_messages()
        return render_template('admin/messages.html', messages=messages)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@admin_messages_bp.route('/admin/messages/open/<uuid:id>', methods=['POST'])
@login_required  
def mark_as_opened(id):
    print("ENTRE A EDITAR EL STATUS")
    print(id)
    put_message_status(str(id))
    return '', 204

