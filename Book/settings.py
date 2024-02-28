
from dotenv import load_dotenv
from os import getenv

load_dotenv()
BOOK_DATABASE_NAME = getenv('BOOK_DATABASE_NAME')
DATABASE_PASSWORD =getenv('DATABASE_PASSWORD')
DATABASE_DIALECT = getenv('DATABASE_DIALECT')
DATABASE_DRIVER = getenv('DATABASE_DRIVER')
DATABASE_USERNAME = getenv('DATABASE_USERNAME')
HOST = getenv('HOST')
DEFAULT_PORT = getenv('DEFAULT_PORT', default='5432')
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
SENDER_EMAIL = getenv('SENDER_EMAIL')
SENDER_PASSWORD = getenv('SENDER_PASSWORD')
REDIS_PORT = getenv('REDIS_PORT')
REDIS_URL = getenv('REDIS_URL')
super_key = getenv('super_key')