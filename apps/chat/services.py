from sqlalchemy.exc import IntegrityError
from core.database import db
from apps.user.models import User
from .models import Chat, Member, Message


def create_chat(user: User, name: str, image: str or None = None):
    try:
        chat = Chat(name=name, image=image)
        chat.save()
        member = Member(chat=chat, member=user, owner=True)
        member.save()
        return chat
    except IntegrityError:
        db.session.rollback()
        return False


def leave_chat(user: User, chat_id: int):
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        return False
    member = chat.members.filter_by(member=user).first()
    if not member:
        return False
    member.delete()
    return chat


def send_message(user: User, text: str, chat_id: int):
    try:
        chat = Chat.query.filter_by(id=chat_id).first()
        if not bool(chat.members.filter_by(member=user).count()):
            raise IntegrityError
        _message = Message(chat=chat, author=user, text=text)
        _message.save()
        return _message
    except IntegrityError:
        db.session.rollback()
        return False


def get_chats(user: User, search: str):
    chats = user.membership.chat.filter(Chat.name.like(f'%{search}%')).order_by(Chat.last_message_date).all()
    return chats


def get_chat(user: User, chat_id: int):
    chat = Chat.query.filter_by(id=chat_id).first()
    if user not in chat.members.member.all():
        return False
    return chat


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
