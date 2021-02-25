from flask import Blueprint, request
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import (jwt_required, jwt_optional,
                                create_access_token, current_user)
from marshmallow import fields

from .serializers import (user_schema, user_short_schema, users_short_schema,
                          message_schema, messages_schema, chat_schema,
                          chats_schema, chat_short_schema, chats_short_schema)
from core.exceptions import InvalidUsage

from apps.user import (models as user_models,
                       services as user_services)
from apps.chat import (models as chat_models,
                       services as chat_services)

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


@blueprint.route('/test', methods=('GET',))
def get_test():
    return 'Hello world!'


@blueprint.route('/users/signup', methods=('POST', 'OPTIONS'))
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


@blueprint.route('/users/signin', methods=('POST', 'OPTIONS'))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def sign_in_user(username: str, password: str, **kwargs):
    result = user_services.sign_in(username, password)
    if result:
        return result
    else:
        raise InvalidUsage.user_not_found()


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/users/me', methods=('GET', 'OPTIONS'))
@jwt_required
@marshal_with(user_schema)
def get_current_user():
    user = current_user
    return user


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/users/me', methods=('PATCH', 'OPTIONS'))
@jwt_required
@use_kwargs(user_short_schema)
@marshal_with(user_short_schema)
def update_current_user_partial(**kwargs):
    if not kwargs:
        raise InvalidUsage.params_are_missed()
    user = current_user
    result = user_services.update_user(user, **kwargs)
    return result


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/user', methods=('GET', 'OPTIONS'))
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
@blueprint.route('/friendship_offers/create/<int:user_id>', methods=('POST', 'OPTIONS'))
@jwt_required
@marshal_with(user_short_schema)
def make_friendship_offer(user_id: int):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friendship_offers/delete/<int:user_id>', methods=('DELETE', 'OPTIONS'))
@jwt_required
@marshal_with(user_short_schema)
def delete_friendship_offer(user_id: int):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friendship_offers_to_me', methods=('GET', 'OPTIONS'))
@jwt_required
@use_kwargs({'search': fields.Str()})
@marshal_with(users_short_schema)
def get_friendship_offers_to_me(search: str = ''):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friends', methods=('GET', 'OPTIONS'))
@jwt_required
@use_kwargs({'search': fields.Str()})
@marshal_with(users_short_schema)
def get_friends(search: str = ''):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/friendship_offers_by_me', methods=('GET', 'OPTIONS'))
@jwt_required
@use_kwargs({'search': fields.Str()})
@marshal_with(users_short_schema)
def get_friendship_offers_by_me(search: str = ''):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/create_chat', methods=('GET', 'OPTIONS'))
@jwt_required
@use_kwargs(chat_schema)
@marshal_with(chat_schema)
def create_chat():
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/leave_chat/<int:chat_id>', methods=('DELETE', 'OPTIONS'))
@jwt_required
def leave_chat(chat_id: int):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chats', methods=('GET', 'OPTIONS'))
@jwt_required
@use_kwargs({'search': fields.Str()})
@marshal_with(chats_short_schema)
def get_chats(search: str = ''):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>', methods=('GET', 'OPTIONS'))
@jwt_required
@marshal_with(chat_schema)
def get_chat(chat_id: int):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/update_chat/<int:chat_id>', methods=('PATCH', 'OPTIONS'))
@jwt_required
@use_kwargs(chat_schema)
@marshal_with(chat_schema)
def update_chat(chat_id: int, **kwargs):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/members', methods=('GET', 'OPTIONS'))
@jwt_required
@marshal_with(users_short_schema)
def get_chat_members(chat_id: int):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/add_member/<int:user_id>', methods=('POST', 'OPTIONS'))
@jwt_required
def add_chat_member(chat_id: int, user_id: int):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/remove_member/<int:user_id>', methods=('DELETE', 'OPTIONS'))
@jwt_required
def remove_chat_member(chat_id: int, user_id: int):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/messages', methods=('GET', 'OPTIONS'))
@jwt_required
@use_kwargs({'id_from': fields.Int(), 'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(messages_schema)
def get_chat_messages(chat_id: int, id_from: int = None, limit: int = 20, offset: int = 0):
    user = current_user
    return '', 200


@doc(description='Token access', params=auth_params_desc)
@blueprint.route('/chat/<int:chat_id>/send_message', methods=('POST', 'OPTIONS'))
@jwt_required
@use_kwargs(message_schema)
@marshal_with(message_schema)
def send_chat_message(chat_id: int, text: str, **kwargs):
    user = current_user
    return '', 200
