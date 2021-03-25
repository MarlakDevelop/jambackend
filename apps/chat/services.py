from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from core.database import db
from apps.user.models import User
from .models import Chat, Member, Message
from apps.user import services as user_services


def create_chat(user: User, name: str, image: str or None = None):
    try:
        chat = Chat(name=name, image=image)
        chat.save()
        member = Member(chat=chat, member=user, owner=True)
        member.save()
        send_message(user=user, text=f'Чат {name} создан', chat_id=chat.id)
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
        if not chat:
            return False
        if not bool(chat.members.filter_by(member=user).count()):
            return False
        _message = Message(chat=chat, author=user, text=text)
        _message.save()
        return _message
    except IntegrityError:
        db.session.rollback()
        return False


def get_chats(user: User, search: str):
    chats = Chat.query.filter((Chat.name.like(f'%{search}%')), (Chat.id.in_([x.chat_id for x in user.membership.all()]))).all()
    chats = list(sorted(chats, key=lambda x: x.last_message_date, reverse=True))
    return chats


def get_chat(user: User, chat_id: int):
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat.members.filter_by(member=user).all():
        return False
    return chat


def update_chat(user: User, chat_id, name: str = '', image: str or None = None, **kwargs):
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        return False
    if not chat.members.filter_by(member=user, owner=True).all():
        return False
    try:
        chat.update(name=name, image=image)
        return chat
    except IntegrityError:
        db.session.rollback()
        return None


def get_chat_members(user: User, chat_id: int):
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        return False
    if not chat.members.filter_by(member=user).all():
        return False
    return list(sorted(chat.members, key=lambda x: x.member.username))


def add_chat_member(user: User, chat_id: int, user_id: int):
    friends = user_services.get_friends(user, '')
    user_new_member = User.query.filter_by(id=user_id).first()
    chat = Chat.query.filter_by(id=chat_id).first()
    if not user_new_member:
        return None
    if user_new_member not in friends:
        return None
    if not chat:
        return False
    if not chat.members.filter_by(member=user).all():
        return False
    if chat.members.filter_by(member=user_new_member).all():
        return False
    member = Member(chat=chat, member=user_new_member, owner=False)
    member.save()
    return member


def remove_chat_member(user: User, chat_id: int, user_id: int):
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        return False
    user_member = chat.members.filter_by(member_id=user_id).first()
    if not user_member:
        return False
    if not chat.members.filter_by(member=user, owner=True).all():
        return False
    user_member.delete()
    return chat


def get_chat_messages(user: User, chat_id: int, id_from: int, offset: int, limit: int):
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        return False
    if not chat.members.filter_by(member=user).all():
        return False
    messages = chat.messages.filter(Message.id >= id_from).offset(offset).limit(limit).all()
    return list(sorted(messages, key=lambda x: x.id, reverse=True))
