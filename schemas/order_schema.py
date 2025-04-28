from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    food_id = fields.Int(required=True)
    quantity = fields.Int(required=True)