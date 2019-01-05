from app import api, db, blacklist
import datetime
from flask import request
from flask_restful import Resource
from .schemas import user_schema
from .models import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt, jwt_optional


class Register(Resource):

    @staticmethod
    def post():
        req_body = request.get_json()
        username, password, email = req_body.get('username'), req_body.get('password'), req_body.get('email')

        if username is None or password is None or email is None:
            return {'error': 'Missing arguments'}
        elif User.query.filter_by(username=username).first() is not None:
            return {'error': 'Username taken'}
        elif User.query.filter_by(email=email).first() is not None:
            return {'error': 'Email is already in use'}

        new_user = user_schema.load({
            'username': username,
            'password_hash': User.hash_password(password)
        })

        db.session.add(new_user)
        db.session.commit()

        # Generate Token
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=username, expires_delta=expires)

        return {
            'access_token': access_token,
            'datasets_owned': [],
            'permissions': {
                'is_admin': new_user.is_admin
            }
        }


class Login(Resource):

    @staticmethod
    def post():
        req_body = request.get_json()
        username, password = req_body.get('username'), req_body.get('password')

        if username is None or password is None:
            return {'error': 'Missing arguments'}

        user = User.query.filter_by(username=username).first()

        if user is not None:
            if user.verify_password(password):
                # Generate Token
                expires = datetime.timedelta(days=1)
                access_token = create_access_token(identity=username, expires_delta=expires)
                return {
                    'access_token': access_token,
                    'user_id': user.id,
                    'permissions': {
                        'is_admin': user.is_admin,
                    }
                }
            else:
                return {'error': 'Credentials provided are incorrect'}
        else:
            return {'error': 'User does not exist'}


class UserView(Resource):

    @jwt_required
    def get(self):
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        return {'result': user_schema.dump(current_user)}


class UserLogoutView(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200


api.add_resource(Register, '/users/register')
api.add_resource(Login, '/users/login')
api.add_resource(UserLogoutView, '/users/logout')
api.add_resource(UserView, '/users/me')