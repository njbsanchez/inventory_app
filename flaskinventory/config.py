# Application Properties
ORG_NAME = 'MJ'
APP_TITLE = 'Sales & Inventory DB'
APP_DESC = 'An extremely simple way to track the sales and inventory of cannabis products.'

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# Flask-Admin config
DEBUG = True
HOST = 'localhost'
PORT = 8000

# database
DATABASE_FILE = 'inventory_psql'
SQLALCHEMY_DATABASE_URI = 'postgresql:///' + DATABASE_FILE
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_LOGGING = False