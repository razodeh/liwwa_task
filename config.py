from datetime import timedelta
from os import environ as ENV

# ...:::Flask:::...
JSON_AS_ASCII = ENV.get("JSON_AS_ASCII", 0)
# ...:::FileStorage:::...
FILE_UPLOAD_PATH = ENV.get('FILE_UPLOAD_PATH', "./uploads/")
# ...:::DB:::...
DB_HOST = ENV.get('DB_HOST', "0.0.0.0")
DB_PORT = ENV.get('DB_PORT', "3307")
DB_NAME = ENV.get('DB_NAME', "tinyhr")
DB_USER = ENV.get('DB_USER', "root")
DB_PASS = ENV.get('DB_PASS', "root")
SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# ...:::JWT:::...
JWT_SECRET_KEY = ENV.get('JWT_SECRET_KEY', 'GA8tz3bVIhkxROkc6mYtY1lyKseL1DpG')
JWT_ACCESS_TOKEN_EXPIRES = ENV.get('JWT_ACCESS_TOKEN_EXPIRES', timedelta(hours=24))
