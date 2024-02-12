from marshmallow import Schema, fields

class PlainItemSchema (Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ItemSchema (PlainItemSchema):
    store = fields.Nested(lambda:PlainStoreSchema(),dump_only=True)
    tags = fields.List(fields.Nested(lambda:PlainTagSchema()), dump_only=True)

class UpdateItemSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Str()


class PlainStoreSchema (Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    url =  fields.Url(required= True)

class StoreSchema (PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(lambda: PlainTagSchema()),dump_only=True)


class UpdateStoreSchema (Schema):
    name = fields.Str(required=True)

class PlainTagSchema (Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    store_id = fields.Int(load_only=True)

class TagSchema (PlainTagSchema):
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(lambda:PlainItemSchema()),dump_only=True)

class ItemsAndTags (Schema):
    tag_id = fields.Int(dump_only=True)
    item_id = fields.Int(dump_only=True)

class ItemAndTagsSchema (Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema (Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)