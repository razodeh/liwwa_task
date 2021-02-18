from schematics import Model
from schematics.types import EmailType, DateType, IntType, ModelType

from extensions import StringType
from models import Department


class LoginParams(Model):
    email = EmailType(required=True)
    password = StringType(min_length=8, required=True)


class Profile(Model):
    years_of_experience = IntType(required=True, min_value=0)
    date_of_birth = DateType(required=True)
    department = StringType(
        choices=Department.choices(),
        required=True
    )


class RegistrationParams(Model):
    email = EmailType(required=True)
    password = StringType(min_length=8, required=True)
    first_name = StringType(min_length=2, required=True)
    last_name = StringType(min_length=2, required=True)
    profile = ModelType(Profile, required=True)
