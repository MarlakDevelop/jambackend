from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (create_access_token)

from core.database import db

from .models import User


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
    try:
        user.update(**kwargs)
        return user
    except IntegrityError:
        db.session.rollback()
        return None


def get_user_by_fields(**kwargs):
    user = User.query.filter_by(**kwargs).first()
    if user is not None:
        return user
    else:
        return None


def make_friendship_offer(user_by: User, user_to_id: int):
    user_to = User.query.filter_by(id=user_to_id).first()
    if not user_to:
        return False
    if user_by.id == user_to.id:
        return False
    if user_to in user_by.friendship_offers.all():
        return False
    user_by.friendship_offers.append(user_to)
    user_by.save()
    return user_to


def remove_friendship_offer(user_by: User, user_to_id: int):
    user_to = User.query.filter_by(id=user_to_id).first()
    if not user_to:
        return False
    if user_to not in user_by.friendship_offers.all():
        return False
    user_by.friendship_offers.remove(user_to)
    user_by.save()
    return user_to


def get_friendship_offers_by(user: User, search: str = ''):
    offers = [x for x in user.friendship_offers.all() if user not in x.friendship_offers.all() and
              search in x.username]
    return offers


def get_friendship_offers_to(user: User, search: str = ''):
    offers = [x for x in user.friendship_offers_to_user.all() if user not in x.friendship_offers_to_user.all() and
              search in x.username]
    return offers


def get_friends(user: User, search: str = ''):
    friends = [x for x in user.friendship_offers.all() if user in x.friendship_offers.all() and search in x.username]
    return friends
