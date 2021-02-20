from datetime import timedelta
from os import environ as ENV

# ...:::Flask:::...
JSON_AS_ASCII = ENV.get("JSON_AS_ASCII", 0)
# ...:::FileStorage:::...
FILE_UPLOAD_PATH = ENV.get('FILE_UPLOAD_PATH', "./uploads/")
# ...:::DB:::...
DB_HOST = ENV.get('DB_HOST', None)
DB_PORT = ENV.get('DB_PORT', None)
DB_NAME = ENV.get('DB_NAME', None)
DB_USER = ENV.get('DB_USER', None)
DB_PASS = ENV.get('DB_PASS', None)
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# ...:::JWT:::...
JWT_SECRET_KEY = ENV.get('JWT_SECRET_KEY', 'GA8tz3bVIhkxROkc6mYtY1lyKseL1DpG')
token_expiration_in_hours = timedelta(hours=int(ENV.get('TOKEN_EXPIRATION_IN_HOURS', 24)))
JWT_ACCESS_TOKEN_EXPIRES = token_expiration_in_hours
