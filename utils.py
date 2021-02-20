import hashlib
import re
from functools import wraps

from flask import request
from flask_jwt_extended import current_user
from schematics.datastructures import FrozenDict
from schematics.exceptions import DataError
from werkzeug.security import gen_salt as salt_generator

from exceptions import TinyHRError


def gen_salt():
    """
    Generates a random salt.
    """
    return salt_generator(17)


def compute_hash(password, salt):
    """
    Computes the SHA256 hash of the given password and encodes the result into
    a hexadecimal string.
    :param password:
    :param salt:
    :return:
    """
    digest = hashlib.sha256(
        password.encode('utf-8') + salt.encode('utf-8')
    ).hexdigest()
    return digest


def required_params(params):
    """
    Decorator to validate request inputs, to match schematic Model.
    :param params:
    :return:
    """

    def serialize_errors(errors):
        """
        Serializes validation messages into JSON serializable format
        """
        serialized = {
            field: serialize_errors(error)
            if isinstance(error, FrozenDict)
            else [str(msg) for msg in error.messages]
            for field, error in dict(errors).items()
        }
        return serialized

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                data = params(request.json)
                data.validate()
            except DataError as err:
                error = serialize_errors(err.messages)
                raise TinyHRError(error)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def admin_required(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if not (current_user and current_user.is_admin):
            raise TinyHRError("You are not allowed to perform this action", 403)
        return fn(*args, **kwargs)

    return decorated_function


def file_types_required(allowed_types=None):
    """
    Decorator for endpoints with file upload, to safe-guard
    these endpoints from uploading files with unwanted file
    types.
    :param allowed_types: a list of allowed mimetypes, if nothing was passed,
    it means no restrictions
    :return:
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.files and allowed_types:
                for filename, file_obj in request.files.items():
                    if file_obj.mimetype not in allowed_types:
                        raise TinyHRError("Uploaded file type is not allowed.", 422)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def is_valid_email(email):
    EMAIL_REGEX = r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$"
    return not not re.search(EMAIL_REGEX, email)


def is_valid_password(password):
    PASS_REGEX = r"^.{8,}$"
    return not not re.search(PASS_REGEX, password)
