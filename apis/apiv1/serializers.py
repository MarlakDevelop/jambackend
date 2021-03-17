from marshmallow import Schema, fields, pre_load, post_dump


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str(load_only=True)
    image = fields.Url()
    token = fields.Str(dump_only=True)
    online = fields.Bool(dump_only=True)

    @pre_load
    def make_user(self, data, **kwargs):
        if not data.get('username', True):
            del data['username']
        if not data.get('image', True):
            del data['image']
        return data

    @post_dump
    def dump_user(self, data, **kwargs):
        return {'user': data}

    class Meta:
        strict = True


class UserShortSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    image = fields.Str()
    online = fields.Bool(dump_only=True)

    @pre_load
    def make_user(self, data, **kwargs):
        return data

    @post_dump
    def dump_user(self, data, **kwargs):
        return {'user': data}

    class Meta:
        strict = True


class UsersShortSchema(UserShortSchema):
    @post_dump
    def dump_user(self, data, **kwargs):
        return {'user': data}

    @post_dump(pass_many=True)
    def dump_users(self, data, **kwargs):
        return {'users': data, 'count': len(data)}


class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    chat_id = fields.Int(dump_only=True)
    text = fields.Str()
    date_created = fields.DateTime(dump_only=True)
    author = fields.Nested(UserShortSchema)

    @pre_load
    def make_message(self, data, **kwargs):
        return data

    @post_dump
    def dump_message(self, data, **kwargs):
        return {'message': data}

    class Meta:
        strict = True


class MessagesSchema(MessageSchema):
    @post_dump
    def dump_message(self, data, **kwargs):
        return {'message': data}

    @post_dump(pass_many=True)
    def dump_messages(self, data, **kwargs):
        return {'messages': data, 'count': len(data)}


class ChatSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    image = fields.Str()
    is_owner = fields.Bool(dump_only=True)

    @pre_load
    def make_chat(self, data, **kwargs):
        return data

    @post_dump
    def dump_chat(self, data, **kwargs):
        return {'chat': data}

    class Meta:
        strict = True


class ChatsSchema(ChatSchema):
    @post_dump
    def dump_chat(self, data, **kwargs):
        return {'chat': data}


class ChatShortSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    image = fields.Str()
    last_message_date = fields.DateTime(dump_only=True)

    @post_dump
    def dump_chat(self, data, **kwargs):
        return {'chat': data}

    class Meta:
        strict = True


class ChatsShortSchema(ChatShortSchema):
    @post_dump
    def dump_chat(self, data, **kwargs):
        return {'chat': data}

    @post_dump(pass_many=True)
    def dump_chats(self, data, **kwargs):
        return {'chats': data, 'count': len(data)}


user_schema = UserSchema(many=False)

user_short_schema = UserShortSchema(many=False)
users_short_schema = UsersShortSchema(many=True)

message_schema = MessageSchema(many=False)
messages_schema = MessagesSchema(many=True)

chat_schema = ChatSchema(many=False)
chats_schema = ChatsSchema(many=True)

chat_short_schema = ChatShortSchema(many=False)
chats_short_schema = ChatsShortSchema(many=True)
