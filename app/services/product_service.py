from app import db
from app.product.model import Product

class ProductService:
    @staticmethod
    def create_product(amount_available, cost, product_name, seller_id):
        new_product = Product(
        amount_available=amount_available,
        cost=cost,
        product_name=product_name,
        seller_id=seller_id)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def get_products():
        return Product.query.all()
    
    @staticmethod
    def get_product_by_id(prod_id):
        return Product.query.get(prod_id)

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        product.amount_available = data['amount_available']
        product.cost = data['cost']
        product.product_name = data['product_name']
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        db.session.delete(product)
        db.session.commit()
        return product

    def bought(prod_id, amount):
        product = Product.query.get(prod_id)
        product.amount_available -= amount
        if product.amount_available == 0:
            db.session.delete(product)
        db.session.commit()
        
