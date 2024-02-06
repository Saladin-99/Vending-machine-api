# app/product/schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validate
from app import ma
from app.product.model import Product


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
    id = ma.auto_field(dump_only=True)
    amount_available = ma.Integer(required=True, validate=validate.Range(min=1, max=100))
    cost = ma.Float(required=True, validate=validate.Range(min=1, max=5000))
    product_name = ma.String(required=True, validate=validate.Length(min=1, max=255))
    seller_id = ma.Integer(dump_only=True, required=True)
