from flask_restful import Resource, abort
from flask import request
from app.models import Product, CartItem
from .extensions import db


class ProductResource(Resource):
    def get(self, product_id=None):
        try:
            if product_id is None:
                # If product_id is not provided, return all products
                products = Product.query.all()
                result = [{'id': product.id, 'name': product.name,
                           'price': product.price, "image_url": product.image_url} for product in products]
                return {"data": result}, 200
            else:
                # If product_id is provided, return the specific product
                product = Product.query.get(product_id)
                if not product:
                    abort(404, message="Product not found")
                return {'id': product.id, 'name': product.name, 'price': product.price, "image_url": product.image_url}, 200
        except Exception as e:
            return {"status": "error", "message": e}

    def post(self):
        try:
            data = request.json
            product = Product(
                name=data['name'], price=data['price'], description=data['description'], image_url=data['image_url'])
            db.session.add(product)
            db.session.commit()
            return {'message': 'Product added successfully'}, 201
        except KeyError:
            abort(400, message="Missing required fields")

    def put(self, product_id):
        product = Product.query.get_or_404(product_id)
        data = request.json
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.description = data.get('description', product.description)
        product.image_url = data.get('image_url', product.image_url)
        db.session.commit()
        return {'message': 'Product updated successfully'}

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}


class CartResource(Resource):
    def get(self, cart_id=None):
        if cart_id is None:
            # If product_id is not provided, return all carts
            carts = CartItem.query.all()
            result = [{'id': cart.id, 'product_id': cart.product_id,
                       'quantity': cart.quantity} for cart in carts]
            return {"data": result}, 200
        else:
            cart = CartItem.query.get_or_404(cart_id)
            return {'product_id': cart.product_id, 'quantity': cart.quantity}

    def post(self):
        try:
            data = request.json
            cart = CartItem(
                product_id=data['product_id'], quantity=data['quantity'])
            db.session.add(cart)
            db.session.commit()
            return {'message': 'Product added to cart successfully'}, 201
        except KeyError:
            abort(400, message="Missing required fields")

    def put(self, cart_id):
        try:
            cart = CartItem.query.get_or_404(cart_id)
            data = request.json
            cart.product_id = data.get('product_id', cart.product_id)
            cart.quantity = data.get('quantity', cart.quantity)
            db.session.commit()
            return {'message': 'Cart updated successfully'}
        except KeyError:
            abort(400, message="Missing required fields")

    def delete(self, cart_id):
        cart = CartItem.query.get_or_404(cart_id)
        db.session.delete(cart)
        db.session.commit()
        return {'message': 'Cart item deleted successfully'}
