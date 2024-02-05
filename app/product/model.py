from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_available = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller = db.relationship('User', backref='products')