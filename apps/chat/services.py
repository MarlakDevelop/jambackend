from sqlalchemy.exc import IntegrityError
from core.database import db
from apps.user.models import User
from .models import Chat, Message


def create_chat(user: User, name: str = 'Chat', image: str or None = None):
    try:
        chat = Chat(name=name, image=image)
        chat.members.append()
    except IntegrityError:
        db.session.rollback()
        return False


def leave_chat(user, chat):
    pass


def send_message(user, message, chat):
    pass


def get_chats(user, search):
    pass


def get_chat(chat_id):
    pass


def update_chat(chat, **kwargs):
    pass


def get_chat_members(chat):
    pass


def get_chat_messages(chat_id, id_from, offset, limit):
    pass


def add_chat_member(chat, user):
    pass


def remove_chat_member(chat, user):
    pass


def is_chat_owner(chat, user):
    pass


def is_chat_member(chat, user):
    pass
