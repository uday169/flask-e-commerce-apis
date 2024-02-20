from flask import Blueprint
from flask_restful import Api
from .resources import ProductResource, CartResource

products_bp = Blueprint('products', __name__)
api = Api(products_bp)

# Add routes for resources
api.add_resource(ProductResource, '/products', '/products/<int:product_id>')
api.add_resource(CartResource, '/cart', '/cart/<int:cart_id>')
