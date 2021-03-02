import datetime as dt

from core.database import (Column, Model,
                           SurrogatePK, db,
                           relationship, reference_col)


member_assoc = db.Table('member_assoc',
                        db.Column('member_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('chat_id', db.Integer, db.ForeignKey('chat.id')),
                        db.Column('owner', db.Boolean, default=False))


class Chat(SurrogatePK, Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    name = Column(db.String(80), nullable=False)
    image = Column(db.String(120), nullable=True)
    messages = relationship(
        'Message',
        backref=db.backref('chats', uselist=False),
        lazy='dynamic'
    )
    members = relationship(
        'User',
        secondary=member_assoc,
        backref=db.backref('chats', uselist=False),
        lazy='dynamic'
    )


class Message(SurrogatePK, Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    text = Column(db.String, nullable=False)
    date_created = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    author_id = reference_col('user', nullable=False)
    author = relationship('User', backref=db.backref('messages'))
