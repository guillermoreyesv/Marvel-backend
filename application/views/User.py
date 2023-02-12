from flask.views import MethodView
from flask import request


class ManageUser(MethodView):
    # Check Profile
    def get(self):
        return 'test'

    # Register User
    def post(self):
        from application.utils.user import User
        from application.config.db import mongo

        # Params Dict
        params_received = request.get_json()

        # Check information
        response_validation = User.custom_validations(params_received)

        # If the information is not valid
        if response_validation['code'] != 200:
            return response_validation, response_validation['code']

        # Sanitize string
        email = params_received['email'].strip().lower()
        password = params_received['password'].strip()
        name = params_received['name'].strip()
        birthday = params_received['birthday']

        # Hash password
        hashed_password = User.hash_password(password=password)

        # Generate document
        user_dict = {
            'email': email,
            'password': hashed_password,
            'name': name,
            'birthday': User.transform_date(birthday)
        }

        # Get users collection
        user_collection = mongo.db.users

        # Check if user is already register
        results = user_collection.find_one({'email': email})
        if results:
            user_dict.pop('password')
            response = {
                'code': 409,
                'status': 'failed',
                'message': 'User is already registered',
                'params': user_dict
            }
            return response, response['code']

        # Save document
        result = user_collection.insert_one(user_dict)

        # Remove sensible information
        user_dict.pop('password')
        user_dict.pop('_id')

        # If document was saved
        if result.acknowledged:
            response = {
                'code': 200,
                'status': 'ok',
                'message': 'User has been registered',
                'params': user_dict
            }
        else:
            response = {
                'code': 500,
                'status': 'failed',
                'message': 'User has not been registered',
                'params': user_dict
            }

        # Response
        return response, response['code']


class Login(MethodView):
    def post(self):
        return 'test'
