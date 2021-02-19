from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required

from exceptions import TinyHRError
from services.user_service import UserService
from utils import admin_required

Candidates = Blueprint('candidates', __name__, url_prefix='/candidates')


@Candidates.route("/", methods=['GET'])
@jwt_required()
@admin_required
def list_all_candidates():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = UserService().list(page, per_page)
    return users


@Candidates.route('/<int:pk>', methods=['GET'])
@jwt_required()
@admin_required
def get_candidate(pk):
    service = UserService()
    user = service.retrieve(pk)
    return service.serialize_listing(user)


@Candidates.route('/<int:pk>/resume', methods=['GET'])
@jwt_required()
@admin_required
def download_candidate_resume(pk):
    resume = UserService().get_user_resume(pk)
    if resume:
        return send_file(
            resume,
            as_attachment=True,
            attachment_filename='resume.pdf',
            mimetype="application/pdf"
        )
    raise TinyHRError("Resume was not uploaded.", 404)
