from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    deposit = db.Column(db.Float, default=0.0)
    role = db.Column(db.String(10), nullable=False)  # 'buyer' or 'seller'
