import uuid
from datetime import datetime
from app import db
from app.models.message import Message


def get_messages():
    return Message.query.order_by(Message.created_at.desc()).all()

def get_message_by_id(id):
    return Message.query.get(id)

def add_message(name,lastname,email,subject,message):
    message = Message(
        id = str(uuid.uuid4()),
        name = name,
        lastname = lastname,
        email = email,
        subject = subject,
        message = message,
        opened = False,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.session.add(message)
    db.session.commit()

    return message

def put_message_status(id):
    message = Message.query.get(id)

    if not message:
        return None

    message.opened = True

    db.session.commit()

    return message

def delete_message(id):
    message = Message.query.get(id)

    if not message:
        return False

    db.session.delete(message)
    db.session.commit()

    return True