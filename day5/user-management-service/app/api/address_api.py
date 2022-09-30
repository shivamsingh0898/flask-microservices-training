from flask import request
from flask_restful import Resource
from ..models.address import Address
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import address_db
from app import api
from app.exceptions import AddressNotFoundException

class AddressApi(Resource):

	def get(self, id):
		conn = get_db_connection()
		address = address_db.get_address_details(conn, id)
		close_db_connection(conn)
		return address

	def put(self, id):
		conn = get_db_connection()
		address_db.get_address_details(conn, id) #validate is address exists befire udpate
		address_db.update_address_details(conn, id, Address.from_json(request.json))
		addresses = address_db.get_address_details(conn, id)
		commit_and_close_db_connection(conn)
		return users

	def delete(self, id):
		conn = get_db_connection()
		address = address_db.get_address_details(conn, id)
		address_db.delete_address(conn, id)
		commit_and_close_db_connection(conn)
		return {'message': f'Address [{address["address_line_1"]}] deleted from the database'}