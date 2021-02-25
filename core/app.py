from flask import Flask
from flask_apispec import FlaskApiSpec
from core.extensions import (bcrypt, cache,
                             db, migrate,
                             jwt, cors)
from core.exceptions import (InvalidUsage)
from apps import (chat, user)
from apis import apiv1


def create_app(config):
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_swagger(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    return app


def register_extensions(app: Flask):
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app: Flask):
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(app=apiv1.views.blueprint, origins=origins)
    app.register_blueprint(apiv1.views.blueprint)


def register_swagger(app: Flask):
    docs = FlaskApiSpec(app)
    docs.register(target=apiv1.views.get_test, blueprint='api_v1')
    docs.register(target=apiv1.views.sign_up_user, blueprint='api_v1')
    docs.register(target=apiv1.views.sign_in_user, blueprint='api_v1')
    docs.register(target=apiv1.views.get_current_user, blueprint='api_v1')
    docs.register(target=apiv1.views.update_current_user_partial, blueprint='api_v1')
    docs.register(target=apiv1.views.get_user_by_fields, blueprint='api_v1')
    docs.register(target=apiv1.views.make_friendship_offer, blueprint='api_v1')
    docs.register(target=apiv1.views.delete_friendship_offer, blueprint='api_v1')
    docs.register(target=apiv1.views.get_friendship_offers_to_me, blueprint='api_v1')
    docs.register(target=apiv1.views.get_friends, blueprint='api_v1')
    docs.register(target=apiv1.views.get_friendship_offers_by_me, blueprint='api_v1')
    docs.register(target=apiv1.views.create_chat, blueprint='api_v1')
    docs.register(target=apiv1.views.leave_chat, blueprint='api_v1')
    docs.register(target=apiv1.views.get_chats, blueprint='api_v1')
    docs.register(target=apiv1.views.get_chat, blueprint='api_v1')
    docs.register(target=apiv1.views.update_chat, blueprint='api_v1')
    docs.register(target=apiv1.views.get_chat_members, blueprint='api_v1')
    docs.register(target=apiv1.views.add_chat_member, blueprint='api_v1')
    docs.register(target=apiv1.views.remove_chat_member, blueprint='api_v1')
    docs.register(target=apiv1.views.get_chat_messages, blueprint='api_v1')
    docs.register(target=apiv1.views.send_chat_message, blueprint='api_v1')


def register_errorhandlers(app: Flask):
    def errorhandler(error: InvalidUsage):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app: Flask):
    def shell_context():
        return {
            'db': db,
            'User': user.models.User,
            'Chat': chat.models.Chat,
            'Message': chat.models.Message,
        }
    app.shell_context_processor(shell_context)
