from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (create_access_token)

from core.database import db

from .models import (User, friendship_offer)


def sign_up(username: str, password: str, **kwargs):
    try:
        user = User(username=username, password=password, **kwargs).save()
        user.token = create_access_token(identity=user)
        return user
    except IntegrityError:
        db.session.rollback()
        return None


def check_sign_up_data(username: str, password: str, **kwargs):
    if len(username) not in range(4, 33):
        return False
    if len(password) not in range(8, 33):
        return False
    return True


def sign_in(username: str, password: str):
    user = User.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        user.token = create_access_token(identity=user, fresh=True)
        return user
    else:
        return None


def check_username_for_unique(username: str):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return False
    return True


def update_user(user: User, **kwargs):
    user.update(**kwargs)
    return user


def get_user_by_fields(**kwargs):
    user = User.query.filter_by(**kwargs).first()
    if user is not None:
        return user
    else:
        return None


def make_friendship_offer(user_by: User, user_to: User):
    pass


def remove_friendship_offer(user_by, user_to):
    pass


def get_friendship_offers_by_me(user: User):
    pass


def get_friendship_offers_to_me(user: User):
    pass


def get_friends(user: User):
    pass
