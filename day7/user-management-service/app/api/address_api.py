from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import address_db
from ..schemas.address_schema import AddressSchema
from ..exceptions import InvalidAddressPayload
from ..models.address import Address
from app import restful_api

address_schema = AddressSchema()

class AddressApi(Resource):
	decorators = [jwt_required()]
	def get(self, id,user_id):
		conn = get_db_connection()
		address = address_db.get_address_details(conn, id,user_id)
		close_db_connection(conn)
		return address

	def put(self, id,user_id):
		conn = get_db_connection()
		address_db.get_address_details(conn, id,user_id) #validate id address exists befire udpate
		address_db.update_address_details(conn, id, Address.from_json(request.json),user_id)
		address = address_db.get_address_details(conn, id,user_id)
		commit_and_close_db_connection(conn)
		return address

	def delete(self, id,user_id):
		conn = get_db_connection()
		address = address_db.get_address_details(conn, id,user_id)
		address_db.delete_address(conn, id,user_id)
		commit_and_close_db_connection(conn)
		return {'message': f'Address [{address["id"]}] deleted from the database'}

restful_api.add_resource(AddressApi, '/api/user/<int:user_id>addresses/<int:id>')