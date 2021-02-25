from marshmallow import Schema, fields, pre_load, post_dump


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str(load_only=True)
    image = fields.Url()
    token = fields.Str(dump_only=True)
    online = fields.Bool()

    @pre_load
    def make_user(self, data, **kwargs):
        print(data)
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
    image = fields.Url()
    online = fields.Bool()

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

    @post_dump(pass_many=True)
    def dump_messages(self, data, **kwargs):
        return {'messages': data, 'count': len(data)}

    class Meta:
        strict = True


class ChatSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    image = fields.Url()
    is_owner = fields.Bool(dump_only=True)

    @pre_load
    def make_chat(self, data, **kwargs):
        return data

    @post_dump
    def dump_chat(self, data, **kwargs):
        return {'chat': data}

    @post_dump(pass_many=True)
    def dump_chats(self, data, **kwargs):
        return {'chats': data, 'count': len(data)}

    class Meta:
        strict = True


class ChatShortSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    image = fields.Url()
    last_message_date = fields.DateTime(dump_only=True)

    @post_dump
    def dump_chat(self, data, **kwargs):
        return {'chat': data}

    @post_dump(pass_many=True)
    def dump_chats(self, data, **kwargs):
        return {'chats': data, 'count': len(data)}

    class Meta:
        strict = True


user_schema = UserSchema()

user_short_schema = UserShortSchema()
users_short_schema = UserShortSchema(many=True)

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)

chat_short_schema = ChatShortSchema()
chats_short_schema = ChatShortSchema(many=True)
