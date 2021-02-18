from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from services.user_service import UserService
from utils import required_params
from validators import LoginParams, RegistrationParams

Auth = Blueprint('auth', __name__, url_prefix='/auth')


@Auth.route('/login', methods=['POST'])
@required_params(LoginParams)
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = UserService().authenticate_user(email, password)
    token = create_access_token(user)
    return jsonify({"token": token})


@Auth.route('/register', methods=['POST'])
@required_params(RegistrationParams)
def register():
    data = request.json
    profile_data = data.pop('profile')
    user = UserService().create(user_details=data, profile_details=profile_data)
    token = create_access_token(user)
    return jsonify({"token": token}), 201
