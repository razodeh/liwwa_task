from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from exceptions import TinyHRError
from services.user_service import UserService
from utils import file_types_required

Resume = Blueprint('resume', __name__, url_prefix='/resume')


@Resume.route("/", methods=['POST'])
@jwt_required()
@file_types_required(allowed_types=['application/pdf'])
def upload_resume():
    if not (request.files and request.files.get('resume', None)):
        raise TinyHRError({"resume": "This field is required"})
    resume_file = request.files.get('resume')
    UserService().upload_resume(current_user, resume_file)
    return {}, 202
