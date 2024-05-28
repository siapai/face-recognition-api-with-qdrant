from marshmallow import Schema, fields
from flask_smorest.fields import Upload


class PlainCompanySchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)


class PlainUserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    fullname = fields.Str(required=True)
    avatar = fields.Str()


class PlainPhotoSchema(Schema):
    id = fields.Str(dump_only=True)
    filename = fields.Str(required=True)
    url_path = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class RecognitionResultSchema(Schema):
    score = fields.Float()
    url_path = fields.Str()


class MultipartFileSchema(Schema):
    file_1 = Upload()


class FormSchema(Schema):
    username = fields.Str(required=True)


class PhotoSchema(PlainPhotoSchema):
    user_id = fields.Str(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)


class UserSchema(PlainUserSchema):
    company = fields.Nested(PlainCompanySchema(), dump_only=True)
    photos = fields.List(fields.Nested(PlainPhotoSchema()), dump_only=True)


class UserUpdateSchema(Schema):
    fullname = fields.Str()
    avatar = fields.Str(allow_none=True)


class CompanySchema(PlainCompanySchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class RecognitionSchema(Schema):
    username = fields.Str(dump_only=True)
    fullname = fields.Str(dump_only=True)
    company_id = fields.Str(dump_only=True)
    url_path = fields.Str(dump_only=True)
    logged_at = fields.DateTime(dump_only=True)
    results = fields.List(fields.Nested(RecognitionResultSchema()), dump_only=True, allow_none=True)
