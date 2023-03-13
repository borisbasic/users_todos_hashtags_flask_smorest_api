from marshmallow import Schema, fields

class BasicToDoSchema(Schema):
    id = fields.Int(dump_only=True)
    to_do = fields.Str(required=True)
    date = fields.Date(required=True)
    user_id = fields.Int(dump_only=True)


class HashtagSchema(Schema):
    id = fields.Int(dump_only=True)
    hashtag = fields.Str(required=True)


class ToDoSchema(BasicToDoSchema):
    hashtags = fields.List(fields.Nested(HashtagSchema))


class RegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    todos = fields.List(fields.Nested(ToDoSchema(), dump_only=True))



class LoginSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required=True)