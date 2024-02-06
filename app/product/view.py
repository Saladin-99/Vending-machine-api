from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from app.product.schema import ProductSchema
from app.services.product_service import ProductService
from app.services.user_service import UserService

product_bp = Blueprint('product', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create Product
@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    if current_user.role != 'seller':
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = product_schema.load(request.json)
    except ValidationError as e:
        # Handle validation errors, e.g., return a meaningful response
        return jsonify({"error": e.messages}), 400
    new_product = ProductService.create_product(
        data['amount_available'],
        data['cost'],
        data['product_name'],
        current_user.id 
    )
    return product_schema.dump(new_product)


@product_bp.route('/', methods=['GET'])
def get_products():
    all_products = ProductService.get_products()
    if all_products:
        return products_schema.dump(all_products),201
    else:
        return jsonify({"empty":"No products to show"}), 403


# Update Product
@product_bp.route('/', methods=['PUT'])
@jwt_required()
def update_product():
    if current_user.role != 'seller':
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    prod_id = data["id"]
    prod=ProductService.get_product_by_id(prod_id)
    if prod.seller_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 401
    else:
        product = ProductService.update_product(prod_id, data)
        return product_schema.dump(product)

# Delete Product
@product_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_product():
    if current_user.role != 'seller':
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    prod_id = data["id"]
    prod=ProductService.get_product_by_id(prod_id)
    if prod.seller_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 401
    else:
        product = ProductService.delete_product(prod_id)
        return product_schema.dump(product)

@product_bp.route('/buy', methods=['POST'])
@jwt_required()
def buy_products():
    if current_user.role != 'buyer':
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    product_id = data.get('product_id')
    amount = data.get('amount', 1)  # Default to 1 if not provided

    # Check if the product exists
    product = ProductService.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    if product.amount_available < amount:
        return jsonify({"error": "Product quantity not available"}), 404
    wallet = UserService.get_wallet(current_user.id)
    total_spent = amount * product.cost
    change = wallet-total_spent
    if change < 0:
        return jsonify({"error": "insufficient funds"}), 404
    ProductService.bought(product_id, amount)
    UserService.buy(current_user.id, total_spent)
    product.amount_available = amount

    return jsonify({
        "total_spent": total_spent,
        "products_purchased": product_schema.dump(product),
        "change": change
    }), 200