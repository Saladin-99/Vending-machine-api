from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, create_access_token, current_user
from app import db
from app.services.user_service import UserService
from app.user.schema import UserSchema
from app import jwt

user_bp = Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    print("Received JWT data:", jwt_data)
    identity = jwt_data["sub"]
    return UserService.get_user_by_id(identity)

@jwt.user_identity_loader
def user_identity_loader(user):
    return user.id

@jwt.expired_token_loader
def expired_token_loader(expired_token):
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_loader(error_string):
    return jsonify({"error": "Invalid token"}), 401

# Create User
@user_bp.route('/register', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        # Handle validation errors, e.g., return a meaningful response
        return jsonify({"error": e.messages}), 400

    print(data)
    new_user = UserService.create_user(data['username'], data['password'], data['role'])
    return user_schema.dump(new_user),201

@user_bp.route('/login', methods=['POST'])
def handle_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    match = UserService.match_user(username, password)
    if match:
        access_token = create_access_token(identity=match)
        return jsonify(access_token=access_token),201
    else:
        return jsonify("Wrong username or password"), 401


# Read Users

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    all_users = UserService.get_users()
    return users_schema.dump(all_users),201


@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_user():
    user_id=current_user.id
    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        # Handle validation errors, e.g., return a meaningful response
        return jsonify({"error": e.messages}), 400
    updated_user = UserService.update_user(user_id, data)
    return user_schema.dump(updated_user),201

# Delete User
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    deleted_user = UserService.delete_user(user_id)
    return user_schema.jsonify(deleted_user)


@user_bp.route('/deposit', methods=['POST'])
@jwt_required()
def deposit_coins():
    try:
        data = request.json
        amount = int(data.get('amount', 0))
        if amount not in [5, 10, 20, 50, 100]:
            return jsonify({"error": "Invalid coin amount. Allowed values: 5, 10, 20, 50, 100"}), 400
    except ValueError:
        return jsonify({"error": "Invalid coin amount. Must be an integer."}), 400
    # Check the role to ensure it's a buyer
    if current_user.role != 'buyer':
        return jsonify({"error": "Unauthorized"}), 401

    # Deposit coins into the vending machine account
    deposit_amount = UserService.deposit_coins(current_user.id, amount)
    return jsonify({"deposit": deposit_amount}), 200
