from flask import Blueprint, request, jsonify
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import (jwt_required, jwt_optional,
                                create_access_token, current_user)
from marshmallow import fields

from .serializers import (user_schema, user_short_schema, users_short_schema,
                          message_schema, messages_schema, member_schema, members_schema,
                          chat_schema, chats_schema, chat_short_schema, chats_short_schema)
from core.exceptions import InvalidUsage

from apps.user import (models as user_models,
                       services as user_services)
from apps.chat import (models as chat_models,
                       services as chat_services)

from flask_socketio import SocketIO, emit
from core.extensions import socketio

auth_params_desc = {
    'Authorization': {
        'description':
        'Authorization HTTP header with JWT access token, like: Authorization: Bearer asdf.qwer.zxcv',
        'in':
        'header',
        'type':
        'string',
        'required':
        True
    }
}
blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@blueprint.route('/users/signup', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def sign_up_user(username: str, password: str, **kwargs):
    checker = user_services.check_sign_up_data(username, password, **kwargs)
    if not checker:
        raise InvalidUsage.sign_up_data_is_invalid()
    result = user_services.sign_up(username, password, **kwargs)
    if result:
        return result
    else:
        raise InvalidUsage.user_already_registered()


@blueprint.route('/users/signin', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def sign_in_user(username: str, password: str, **kwargs):
    result = user_services.sign_in(username, password)
    if result:
        return result
    else:
        raise InvalidUsage.user_not_found()


@blueprint.route('/users/check_username_for_unique/<username>', methods=('GET', 'OPTIONS'))
def check_username_for_unique(username: str, **kwargs):
    return jsonify(user_services.check_username_for_unique(username))


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/users/me', methods=('GET',))
@jwt_required
@marshal_with(user_schema)
def get_current_user():
    user = current_user
    return user


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/users/me', methods=('PATCH',))
@jwt_required
@use_kwargs(user_short_schema)
@marshal_with(user_short_schema)
def update_current_user_partial(**kwargs):
    user = current_user
    if not kwargs['image']:
        del kwargs['image']
    elif (len(kwargs['image'].split('image/jpeg')) == 1 and
          len(kwargs['image'].split('image/png')) == 1 and
          len(kwargs['image'].split('image/jpg')) == 1):
        del kwargs['image']
    if not kwargs['username']:
        del kwargs['username']
    if len(kwargs['username']) not in range(4, 33):
        raise InvalidUsage.name_len_is_invalid()
    result = user_services.update_user(user, **kwargs)
    if result:
        return result
    else:
        raise InvalidUsage.username_already_exists()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/user', methods=('GET',))
@jwt_required
@use_kwargs(user_short_schema)
@marshal_with(user_short_schema)
def get_user_by_fields(**kwargs):
    if not kwargs:
        raise InvalidUsage.params_are_missed()
    result = user_services.get_user_by_fields(**kwargs)
    if result:
        return result
    else:
        raise InvalidUsage.user_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friendship_offers/create/<int:user_id>', methods=('POST',))
@jwt_required
@marshal_with(user_short_schema)
def make_friendship_offer(user_id: int):
    user = current_user
    result = user_services.make_friendship_offer(user, user_id)
    if result:
        return result
    else:
        raise InvalidUsage.user_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friendship_offers/delete/<int:user_id>', methods=('DELETE',))
@jwt_required
@marshal_with(user_short_schema)
def delete_friendship_offer(user_id: int):
    user = current_user
    result = user_services.remove_friendship_offer(user, user_id)
    if result:
        return result
    else:
        raise InvalidUsage.user_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friendship_offers_to_me', methods=('GET',))
@jwt_required
@use_kwargs({'search': fields.Str()}, location='query')
@marshal_with(users_short_schema)
def get_friendship_offers_to_me(search: str = ''):
    user = current_user
    result = user_services.get_friendship_offers_to(user, search)
    return result


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friends', methods=('GET',))
@jwt_required
@use_kwargs({'search': fields.Str()}, location='query')
@marshal_with(users_short_schema)
def get_friends(search: str = ''):
    user = current_user
    result = user_services.get_friends(user, search)
    return result


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friendship_offers_by_me', methods=('GET',))
@jwt_required
@use_kwargs({'search': fields.Str()}, location='query')
@marshal_with(users_short_schema)
def get_friendship_offers_by_me(search: str = ''):
    user = current_user
    result = user_services.get_friendship_offers_by(user, search)
    return result


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/create_chat', methods=('POST',))
@jwt_required
@use_kwargs(chat_schema)
@marshal_with(chat_schema)
def create_chat(**kwargs):
    user = current_user
    if not kwargs['image']:
        del kwargs['image']
    elif (len(kwargs['image'].split('image/jpeg')) == 1 and
          len(kwargs['image'].split('image/png')) == 1 and
          len(kwargs['image'].split('image/jpg')) == 1):
        del kwargs['image']
    if not kwargs['name']:
        del kwargs['name']
    if len(kwargs['name']) not in range(4, 33):
        raise InvalidUsage.name_len_is_invalid()
    result = chat_services.create_chat(user, **kwargs)
    if result:
        return result
    else:
        raise InvalidUsage.unknown_error()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/leave_chat/<int:chat_id>', methods=('DELETE',))
@jwt_required
@marshal_with(chat_short_schema)
def leave_chat(chat_id: int):
    user = current_user
    result = chat_services.leave_chat(user, chat_id)
    if result:
        return result
    else:
        raise InvalidUsage.chat_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chats', methods=('GET',))
@jwt_required
@use_kwargs({'search': fields.Str()}, location='query')
@marshal_with(chats_short_schema)
def get_chats(search: str = ''):
    user = current_user
    result = chat_services.get_chats(user, search)
    return result


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>', methods=('GET',))
@jwt_required
@marshal_with(chat_schema)
def get_chat(chat_id: int):
    user = current_user
    result = chat_services.get_chat(user, chat_id)
    if result:
        return result
    else:
        raise InvalidUsage.chat_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/update_chat/<int:chat_id>', methods=('PATCH',))
@jwt_required
@use_kwargs(chat_schema)
@marshal_with(chat_schema)
def update_chat(chat_id: int, **kwargs):
    user = current_user
    if not kwargs['image']:
        del kwargs['image']
    elif (len(kwargs['image'].split('image/jpeg')) == 1 and
          len(kwargs['image'].split('image/png')) == 1 and
          len(kwargs['image'].split('image/jpg')) == 1):
        del kwargs['image']
    if not kwargs['name']:
        del kwargs['name']
    if len(kwargs['name']) not in range(4, 33):
        raise InvalidUsage.name_len_is_invalid()
    result = chat_services.update_chat(user, chat_id, **kwargs)
    if result:
        return result
    else:
        raise InvalidUsage.chat_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/members', methods=('GET',))
@jwt_required
@marshal_with(members_schema)
def get_chat_members(chat_id: int):
    user = current_user
    result = chat_services.get_chat_members(user, chat_id)
    if result:
        return result
    else:
        raise InvalidUsage.chat_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/add_member/<int:user_id>', methods=('POST',))
@jwt_required
@marshal_with(member_schema)
def add_chat_member(chat_id: int, user_id: int):
    user = current_user
    result = chat_services.add_chat_member(user, chat_id, user_id)
    if result:
        return result
    elif result is None:
        raise InvalidUsage.user_not_found()
    else:
        raise InvalidUsage.chat_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/remove_member/<int:user_id>', methods=('DELETE',))
@jwt_required
@marshal_with(chat_schema)
def remove_chat_member(chat_id: int, user_id: int):
    user = current_user
    result = chat_services.remove_chat_member(user, chat_id, user_id)
    if result:
        return result
    else:
        raise InvalidUsage.chat_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/messages', methods=('GET',))
@jwt_required
@use_kwargs({'id_from': fields.Int(), 'limit': fields.Int(), 'offset': fields.Int()}, location='query')
@marshal_with(messages_schema)
def get_chat_messages(chat_id: int, id_from: int = None, limit: int = 20, offset: int = 0):
    user = current_user
    result = chat_services.get_chat_messages(user, chat_id, id_from, offset, limit)
    if result is not False:
        return result
    else:
        raise InvalidUsage.chat_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/send_message', methods=('POST',))
@jwt_required
@use_kwargs(message_schema)
@marshal_with(message_schema)
def send_chat_message(chat_id: int, text: str, **kwargs):
    user = current_user
    result = chat_services.send_message(user, text, chat_id)
    if result:
        return result
    else:
        raise InvalidUsage.chat_not_found()


@socketio.on('user_connect')
def user_connect():
    emit()


@socketio.on('user_disconnect')
def user_disconnect():
    emit()