import hashlib
from functools import wraps

from flask import request
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
