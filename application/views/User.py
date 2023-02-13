from flask.views import MethodView
from flask import request


class ManageUser(MethodView):
    # Check Profile
    def get(self):
        from application import app
        from application.utils.user import User

        # Get Bearer Token
        authorization = request.headers.get('Authorization')

        # Validate Token
        info_user = User.validate_token(authorization)
        if info_user is None:
            response = {
                'code': 401,
                'status': 'error',
                'message': 'Not a valid token.'
            }
            return response, response['code']

        # Preparing profile
        age = User.get_age(info_user['birthday'])
        response = {
            'id': str(info_user.get('_id')),
            'name': info_user.get('name'),
            'age': age,
            'token': info_user.get('access_token')
        }
        app.logger.debug(f'User.ManageUser.post {response}')
        return response, 200

    # Register User
    def post(self):
        from application.utils.user import User
        from application.config.db import mongo
        from application.utils.request import Request
        from application import app

        # Params Dict
        status, params_received = Request.get_json(request)
        if not status:
            return params_received, params_received['code']

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
        try:
            user_collection = mongo.db.users
        except Exception as e:
            app.logger.error(f'User.ManageUser.post.mongo_error.collection {e}')
            response = {
                'code': 500,
                'status': 'error',
                'message': 'Server error.'
            }
            return response, response['code']

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
            app.logger.warning(f'User.ManageUser.post {response}')
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
            app.logger.debug(f'User.ManageUser.post {response}')
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
        from application.utils.user import User
        from application.config.db import mongo
        from application.utils.request import Request
        from flask_jwt_extended import create_access_token
        from application import app

        # Params Dict
        status, params_received = Request.get_json(request)
        if not status:
            return params_received, params_received['code']

        email = params_received.get('email', '').strip().lower()
        password = params_received.get('password', '').strip()

        # Check email and password length
        if len(email) == 0 or len(password) == 0:
            response = {
                'code': 400,
                'status': 'failed',
                'message': 'User or password empty.'
            }
            app.logger.warning(f'User.Login.post params:{params_received} response:{response}')
            return response, response['code']

        # Hash password
        hashed_password = User.hash_password(password=password)

        # Get users collection
        try:
            user_collection = mongo.db.users
        except Exception as e:
            app.logger.error('User.Login.post.mongo_error.collection', e)
            response = {
                'code': 500,
                'status': 'error',
                'message': 'Server error.'
            }
            return response, response['code']

        # Find user document
        dict_to_find = {'email': email, 'password': hashed_password}
        user = user_collection.find_one(dict_to_find)

        # If not found document
        if not user:
            response = {
                'code': 404,
                'status': 'failed',
                'message': 'User not found or password incorrect.'
            }
            app.logger.warning(f'User.Login.post params:{params_received} response:{response}')
            return response, response['code']

        # Create the access token
        access_token = create_access_token(identity=email)

        # Save token
        dict_to_match = {'_id': user['_id']}
        dict_to_update = {'$set': {'access_token': access_token}}
        result = user_collection.update_one(dict_to_match, dict_to_update)

        # Check result
        if result.acknowledged:
            response = {
                'token': access_token,
                'email': email,
                'code': 200,
                'message': 'ok'
            }
            app.logger.debug(f'User.Login.post {response}')

        else:
            response = {
                'code': 500,
                'email': email,
                'message': 'Server error'
            }
            app.logger.error(f'User.Login.post {response}')
        return response, response['code']


class AsignComic(MethodView):
    def post(self):
        from application import app
        from application.utils.user import User
        from application.utils.request import Request
        from application.utils.comics import Comics

        # Get Bearer Token
        authorization = request.headers.get('Authorization')

        # Validate Token
        info_user, user_collection = User.validate_token(authorization)
        if info_user is None:
            response = {
                'code': 401,
                'status': 'error',
                'message': 'Not a valid token.'
            }
            return response, response['code']

        # Params Dict
        status, params_received = Request.get_json(request)
        if not status:
            return params_received, params_received['code']

        # Comics
        comics_list = params_received.get('comics_list', [])

        # Sanitize Comics
        comic_list_cleaned = []
        try:
            for comic_id in comics_list:
                # Only accept Marvels Comics ids
                comic_id_int = int(comic_id)
                Comics.get_comics_by_id(id=comic_id_int)
                comic_list_cleaned.append(comic_id_int)
        except Exception as e:
            response = {
                'code': 400,
                'comic_list': comics_list,
                'message': str(e)
            }
            app.logger.error('User.Login.post', e)
            return response, response['code']

        # Save token
        dict_to_match = {'_id': info_user['_id']}
        dict_to_update = {
            '$addToSet': {
                'comics_layaway': {
                    '$each': comic_list_cleaned
                    }
                }
            }
        result = user_collection.update_one(dict_to_match, dict_to_update)

        # Check result
        if result.acknowledged and result.modified_count:
            response = {
                'comic_list': comics_list,
                'code': 201,
                'message': 'Comics layawayed'
            }
            app.logger.debug(f'User.Login.post {response}')
        elif result.modified_count == 0:
            response = {
                'code': 200,
                'comic_list': comics_list,
                'message': 'Comics already layawayed'
            }
            app.logger.debug(f'User.Login.post {response}')
        else:
            response = {
                'code': 500,
                'comic_list': comics_list,
                'message': 'Server error'
            }
            app.logger.error(f'User.Login.post {response}')
        return response, response['code']


class ViewAssignedComics(MethodView):
    def get(self):
        return 'comics'
