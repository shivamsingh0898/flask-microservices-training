from flask import request
from flask_restful import Resource
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import address_db
from ..schemas.address_schema import AddressSchema
from ..exceptions import InvalidUserPayload
from ..models.address import Address


address_schema = AddressSchema()

class AddressesApi(Resource):

	def get(self):
		conn = get_db_connection()
		addresses = address_db.get_addresses(conn)
		close_db_connection(conn)
		return addresses

	def post(self):
		errors = address_schema.validate(request.json)
		print("errors: "+str(errors))
		if errors:
			raise InvalidUserPayload(errors, 400)
	
		conn = get_db_connection()
		address_db.create_address(conn, Address.from_json(request.json))
		addresses = address_db.get_addresses(conn)
		commit_and_close_db_connection(conn)
		return addresses, 201

	def put(self):
		return {'message': 'Hello PUT'}

	def delete(self):
		return {'message': 'Hello DELETE'}