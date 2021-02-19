from flask import Blueprint, request
from flask_jwt_extended import jwt_required

Resume = Blueprint('resume', __name__, url_prefix='resume')


# @Resume.route("/", methods=['POST'])
# @jwt_required()
# def upload_resume():
#     pass
