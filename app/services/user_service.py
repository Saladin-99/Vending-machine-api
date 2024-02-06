from app import db
from app.user.model import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    @staticmethod
    def create_user(username, password, role):
        new_user = User(username=username, password=generate_password_hash(password), role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(id):
        user = User.query.get(id)
        return user

    def match_user(usern, passw):
        user = User.query.filter_by(username=usern).first()
        if user and check_password_hash(user.password, passw):
            return user
        else:
            return False

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        user.username = data['username']
        user.password = generate_password_hash(data['password'])
        user.role = data['role']
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return user

    @staticmethod
    def deposit_coins(user_id, amount):
        user = User.query.get(user_id)

        # Deposit coins into the vending machine account
        user.deposit += amount
        db.session.commit()
        return user.deposit
    
    @staticmethod
    def bankrupt(user_id):
        user = User.query.get(user_id)

        # Deposit coins into the vending machine account
        user.deposit=0
        db.session.commit()

    @staticmethod
    def get_wallet(user_id):
        user = User.query.get(user_id)
        return user.deposit
    
    @staticmethod
    def buy(user_id, cost):
        user = User.query.get(user_id)
        user.deposit -= cost
        db.session.commit()