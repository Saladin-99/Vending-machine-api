from logging import exception
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, create_access_token, current_user
from app import db
from app.services.user_service import UserService
from app.user.schema import UserSchema
from app import jwt
from app.logconfig import logger

user_bp = Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserService.get_user_by_id(identity)

@jwt.user_identity_loader
def user_identity_loader(user):
    return user.id

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"error": "Token has expired"}), 401

# Custom error handler for JWT errors
@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({"error": "Invalid token"}), 401

@jwt.unauthorized_loader
def unauthorized_callback():
    return jsonify({"error": "Missing Authorization Header"}), 401

# Create User
@user_bp.route('/register', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.json)
        new_user = UserService.create_user(data['username'], data['password'], data['role'])
        logger.info(f"User {new_user.username} created successfully.")
        return user_schema.dump(new_user), 201
        
    except ValidationError as e:
        # Handle validation errors, e.g., return a meaningful response
        logger.error(f"Validation error: {e.messages}")
        return jsonify({"error": e.messages}), 400

    except Exception as e:
        logger.error(f"An error occurred while creating user: {str(e)}")
        return jsonify({"error": "An error occurred while creating user."}), 500


@user_bp.route('/login', methods=['POST'])
def handle_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    match = UserService.match_user(username, password)
    try:
        if match:
            access_token = create_access_token(identity=match)
            logger.info(f"User {username} login successfully and has received access token: {access_token}.")
            return jsonify(access_token=access_token),201
        else:
            return jsonify({"error":"Wrong username or password"}), 401
    except Exception as e:
        logger.error(f"An error occurred while logging in: {str(e)}")
        return jsonify({"error": "An error occurred while logging in. Please try again later."}), 500


# Read Users

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    try:
        all_users = UserService.get_users()
        if all_users:
            logger.info(f"Users returned successfully as requested by {current_user.username}.")
            return users_schema.dump(all_users),201
        else:
            return jsonify({"empty":"No users to show."}), 403
    except Exception as e:
        logger.error(f"An error occurred while getting users: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving userlist. Please try again later."}), 500


@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_user():
    user_id=current_user.id
    try:
        data = user_schema.load(request.json)
        updated_user = UserService.update_user(user_id, data)
        logger.info(f"User {data['username']} information updated successfully.")
        return user_schema.dump(updated_user),201
    except ValidationError as e:
        # Handle validation errors, e.g., return a meaningful response
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"An error occurred while updating user: {str(e)}")
        return jsonify({"error": "An error occurred while updating your user. Please try again later."}), 500

# Delete User
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        deleted_user = UserService.delete_user(user_id)
        logger.info(f"User {current_user.username} deleted user with id {deleted_user.id}.")
        return user_schema.jsonify(deleted_user)
    except Exception as e:
        logger.error(f"An error occurred while deleted user: {str(e)}")
        return jsonify({"error": "An error occurred while deleting user. Please try again later."}), 500

@user_bp.route('/deposit', methods=['POST'])
@jwt_required()
def deposit_coins():

    if current_user.role != 'buyer':
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        amount = int(data.get('amount', 0))
        if amount not in [5, 10, 20, 50, 100]:
            return jsonify({"error": "Invalid coin amount. Allowed values: 5, 10, 20, 50, 100"}), 400
        # Deposit coins into the vending machine account
        deposit_amount = UserService.deposit_coins(current_user.id, amount)
        logger.info(f"User {current_user.username} deposited amount of {deposit_amount} successfully.")
        return jsonify({"deposit": deposit_amount}), 200
    except ValueError:
        return jsonify({"error": "Invalid coin amount. Must be an integer."}), 400

    except Exception as e:
        logger.error(f"An error occurred while depositing: {str(e)}")
        return jsonify({"error": "An error occurred while depositing value. Please try again later."}), 500
    

    

@user_bp.route('/reset', methods=['GET'])
@jwt_required()
def reset_wallet():
    if current_user.role != 'buyer':
        return jsonify({"error": "Unauthorized"}), 401
    try:
        UserService.bankrupt(current_user.id)
        return jsonify({"message": "reset successful"}),201
    except Exception as e:
        logger.error(f"An error occurred while reseting deposit of {current_user.username}: {str(e)}")
        return jsonify({"error": "An error occurred while reseting deposit value. Please try again later."}), 500