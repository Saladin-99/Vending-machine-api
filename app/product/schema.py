# app/product/schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import ma
from app.product.model import Product

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
