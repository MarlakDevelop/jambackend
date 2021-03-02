from core.database import (Column, Model,
                           SurrogatePK, db,
                           relationship)
from core.extensions import bcrypt


friendship_offer = db.Table('friendship_offer',
                            db.Column('offered_to', db.Integer, db.ForeignKey('user.id')),
                            db.Column('offered_by', db.Integer, db.ForeignKey('user.id')))


class User(SurrogatePK, Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)
    online = Column(db.Boolean, default=False, nullable=False)
    image = Column(db.String(120), nullable=True)
    friendship_offers = relationship('User',
                                     secondary=friendship_offer,
                                     primaryjoin=id == friendship_offer.c.offered_to,
                                     secondaryjoin=id == friendship_offer.c.offered_by,
                                     backref='offered_by',
                                     lazy='dynamic'
                                     )
    token: str = ''

    def __init__(self, username, password, **kwargs):
        db.Model.__init__(self, username=username, **kwargs)
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        return f'<User({self.id})>'
