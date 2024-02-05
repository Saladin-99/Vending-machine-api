from app import db
from app.product.model import Product
from flask import current_app

class ProductService:
    @staticmethod
    def create_product(amount_available, cost, product_name, seller_id):
        with current_app.app_context():
            new_product = Product(
                amount_available=amount_available,
                cost=cost,
                product_name=product_name,
                seller_id=seller_id
            )
            db.session.add(new_product)
            db.session.commit()
            return new_product

    @staticmethod
    def get_products():
        with current_app.app_context():
            return Product.query.all()

    @staticmethod
    def update_product(product_id, data):
        with current_app.app_context():
            product = Product.query.get(product_id)
            product.amount_available = data['amount_available']
            product.cost = data['cost']
            product.product_name = data['product_name']
            db.session.commit()
            return product

    @staticmethod
    def delete_product(product_id):
        with current_app.app_context():
            product = Product.query.get(product_id)
            db.session.delete(product)
            db.session.commit()
            return product
