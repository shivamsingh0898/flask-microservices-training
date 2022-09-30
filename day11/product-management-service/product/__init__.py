from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

product = Flask(__name__)
load_configuration(product)

class CustomApi(Api):
    def handle_error(self, e):
        return {'code': e.code, 'message': 'error', 'errors': e.message}, e.code
restful_api = CustomApi(product)


db = SQLAlchemy(product)  


## Imports are essential for python interpreter to find the model files for migration
from .models import product_models