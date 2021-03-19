import datetime as dt

from flask_jwt_extended import current_user
from core.database import (Column, Model,
                           SurrogatePK, db,
                           relationship, reference_col)


class Chat(SurrogatePK, Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    name = Column(db.String(80), nullable=False)
    image = Column(db.Text, nullable=True)

    def __init__(self, name, image, **kwargs):
        db.Model.__init__(self, name=name, image=image, **kwargs)

    @property
    def is_owner(self) -> bool:
        if current_user:
            return bool(Member.query.filter_by(member=current_user, chat_id=self.id, owner=True).count())
        return False

    @property
    def last_message_date(self):
        last_message = Chat.query.filter_by(id=self.id).first().messages.order_by(Message.date_created.desc()).first()
        if not last_message:
            return None
        return last_message.date_created


class Member(SurrogatePK, Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    member_id = reference_col('user', nullable=False)
    member = relationship('User',
                          backref=db.backref('membership', lazy='dynamic'))
    chat_id = reference_col('chat', nullable=False)
    chat = relationship('Chat',
                        backref=db.backref('members', lazy='dynamic'))
    owner = Column(db.Boolean, default=False)

    def __init__(self, member, chat, owner, **kwargs):
        db.Model.__init__(self, member=member, chat=chat, owner=owner, **kwargs)


class Message(SurrogatePK, Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    text = Column(db.String, nullable=False)
    date_created = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    chat_id = reference_col('chat', nullable=False)
    chat = relationship('Chat',
                        backref=db.backref('messages', lazy='dynamic'))
    author_id = reference_col('user', nullable=False)
    author = relationship('User',
                          backref=db.backref('messages', lazy='dynamic'))

    def __init__(self, author, chat, text, **kwargs):
        db.Model.__init__(self, author=author, chat=chat, text=text, **kwargs)
