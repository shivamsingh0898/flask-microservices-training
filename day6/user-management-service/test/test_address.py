import unittest
import app
import init_db

unittest.TestLoader.sortTestMethodsUsing = None

REGISTRATION_URL = '/api/register'
AUTH_URL = '/api/auth'
ADDRESSES_URL = '/api/addresses'

DB_NAME = 'user-management-UT.db';

class UserTest(unittest.TestCase):
    def setUp(self):
        #Initializing Table Schema
        init_db.initialize(DB_NAME)
        self.app = app.app
        self.app.testing = True
        #Pointing to UT database. Can also be handled via environment config
        self.app.config['DATABASE_URI'] = DB_NAME
        self.client = self.app.test_client()
        #Create a test user who's credential will be used for authentication
        self.client.post(REGISTRATION_URL, json = {"name": "test user", "email": "test@user.com", "age": 33, "password": "test"})
        #Generate auth token and save in a class level property
        auth_response = self.client.post(AUTH_URL, json={"email": "test@user.com", "password": "test"})
        self.access_token = auth_response.json['access_token']

        #creating a default address before every testcase
        self.client.post(ADDRESSES_URL, json = {"address_line_1": "123", "city": "Bangalore", "state": "KA", "pin": 560035}, headers = {"Authorization": f"Bearer {self.access_token}"})
    

    def test_get_addresses(self):
        #validate that one address is returned in the response
        response = self.client.get(ADDRESSES_URL, headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)


    def test_create_address_success(self):
        #validate successful creation and total 2 address in DB
        response = self.client.post(ADDRESSES_URL, json = {"address_line_1": "123", "city": "Bangalore", "state": "KA", "pin": 560035}, headers = {"Authorization": f"Bearer {self.access_token}"})
        print(f"API Response: {response.json}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 2)


    def test_create_address_invalid_state_error(self):
        #validate state code error when using a invalid 2 digit state code
        response = self.client.post(ADDRESSES_URL, json = {"address_line_1": "123", "city": "Bangalore", "state": "AB", "pin": 560035}, headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 400)


    def test_get_address_detail(self):
        #validate the address details againt the address_line_1 field
        response = self.client.get(ADDRESSES_URL+"/1", headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("state"), "KA")


    def test_update_address_detail(self):
        #validate the address details againt the address_line_1 field after updating it using PUT
        response = self.client.put(ADDRESSES_URL+"/1", json= {"address_line_1": "123", "city": "Bangalore", "state": "KA", "pin": 560035}, headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("state"), "KA")


    def test_delete_address(self):
        #validate the address is not present in DB after deleting
        delete_response = self.client.delete(ADDRESSES_URL+"/1", headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(delete_response.status_code, 200)
        get_response = self.client.get(ADDRESSES_URL, headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(len(get_response.json), 0)


if __name__ == "__main__":
    unittest.main() 