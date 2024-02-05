from flask import Blueprint, request, jsonify
from app.product.schema import ProductSchema
from app.services.product_service import ProductService

product_bp = Blueprint('product', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create Product
@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = ProductService.create_product(data['amount_available'], data['cost'], data['product_name'], data['seller_id'])
    return product_schema.jsonify(new_product)

# Read Products
@product_bp.route('/products', methods=['GET'])
def get_products():
    all_products = ProductService.get_products()
    return products_schema.jsonify(all_products)

# Update Product
@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = ProductService.update_product(product_id, data)
    return product_schema.jsonify(product)

# Delete Product
@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ProductService.delete_product(product_id)
    return product_schema.jsonify(product)
