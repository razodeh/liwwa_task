from datetime import datetime
from enum import Enum

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp

from utils import compute_hash, gen_salt

DB = SQLAlchemy()
migrate = Migrate()


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    password = DB.Column(DB.String(128), nullable=False)
    first_name = DB.Column(DB.String(128))
    last_name = DB.Column(DB.String(128))
    is_admin = DB.Column(DB.Boolean, nullable=False, default=False)
    date_joined = DB.Column(DB.Date(), default=datetime.utcnow)
    profile = DB.relationship('CandidateProfile', backref='user', uselist=False)
    salt = DB.Column(DB.String(17), nullable=False, default=gen_salt)

    def authenticate(self, password):
        pass_hash = compute_hash(password, self.salt)
        return safe_str_cmp(self.password.encode('utf-8'), pass_hash.encode('utf-8'))

    def hashify_password(self, password):
        self.password = compute_hash(password, self.salt)


class Department(Enum):
    it = 0
    hr = 1
    finance = 3

    @classmethod
    def choices(cls):
        return list(dict(cls.__members__).keys())


class CandidateProfile(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    years_of_experience = DB.Column(DB.Integer, nullable=False)
    date_of_birth = DB.Column(DB.Date, nullable=False)
    resume_url = DB.Column(DB.String(254))
    department = DB.Column(DB.Enum(Department), nullable=False)
