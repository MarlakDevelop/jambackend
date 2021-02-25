import datetime as dt

from core.database import (Column, Model,
                           SurrogatePK, db,
                           relationship, reference_col)


member_assoc = db.Table('member_assoc',
                        db.Column('member', db.Integer, db.ForeignKey('user.id')),
                        db.Column('chat', db.Integer, db.ForeignKey('chat.id')),
                        db.Column('owner', db.Boolean, default=False))


class Chat(SurrogatePK, Model):
    __tablename__ = 'chat'

    name = Column(db.String(80), nullable=False)
    image = Column(db.String(120), nullable=True)
    messages = relationship(
        'Message',
        backref='chats',
        lazy='dynamic'
    )
    members = relationship(
        'User',
        secondary=member_assoc,
        backref='chats',
        lazy='dynamic'
    )


class Message(SurrogatePK, Model):
    __tablename__ = 'message'

    text = Column(db.String, nullable=False)
    date_created = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    author_id = reference_col('user', nullable=False)
    author = relationship('User', backref=db.backref('messages'))
