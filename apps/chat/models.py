import datetime as dt

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


class Member(SurrogatePK, Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    member_id = reference_col('user', nullable=False)
    member = relationship('Chat', backref=db.backref('membership'))
    chat_id = reference_col('chat', nullable=False)
    chat = relationship('Chat', backref=db.backref('members'))
    owner = Column(db.Boolean, default=False)


class Message(SurrogatePK, Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    text = Column(db.String, nullable=False)
    date_created = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    chat_id = reference_col('chat', nullable=False)
    chat = relationship('Chat', backref=db.backref('messages'))
    author_id = reference_col('user', nullable=False)
    author = relationship('User', backref=db.backref('messages'))
