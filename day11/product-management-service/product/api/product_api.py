from flask import request
from flask_restful import Resource
from ..models.product_models import Product
from product import restful_api, db
#from ..database import user_db
#from ..schemas.user_schema import UserSchema

#user_schema = UserSchema()

class ProductApi(Resource):
	def get(self, id):
		product = Product.query.get(id)
		if not product:
			raise ProductNotFoundException(f"Product with ID [{id}] not found in DB")
		return Product.to_json()

	def put(self, id):
		product = Product.query.get(id)
		if not product:
			raise ProductNotFoundException(f"User with ID [{id}] not found in DB")
		errors = product_schema.validate(request.json)
		if errors:
			raise InvalidProductPayload(errors, 400)
		updated_product = Product.from_json(request.json)
		product.name = updated_product.name
		product.description = updated_product.description
		product.price = updated_product.price
		product.currency = updated_product.currency
		product.stock = updated_product.stock
		product.active = updated_product.active
		db.session.commit()
		return product.to_json()

	def delete(self, id):
		product = Product.query.get(id)
		db.session.delete(product)
		db.session.commit()
		return {'message': f'Product [{product.description}] deleted from the database'}

restful_api.add_resource(ProductApi, '/api/products/<int:id>')