from app import app, api
from app.api.users_api import UsersApi
from app.api.user_api import UserApi
from app.api.user_api import UserApi
from app.api.addresses_api import AddressesApi
from app.api.address_api import AddressApi
from app.api.auth_api import AuthApi, ProtectedApi

if __name__ == '__main__':
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/users/<int:id>')
    api.add_resource(AuthApi, '/api/auth')
    api.add_resource(ProtectedApi, '/api/protected')
    api.add_resource(AddressesApi, '/api/addresses')
    api.add_resource(AddressApi, '/api/addresses/<int:id>')
    app.run()