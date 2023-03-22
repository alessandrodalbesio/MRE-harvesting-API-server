import os

# Flask settings
HOST = 'localhost'
PORT = 5000
STATIC_URL_PATH = '/'
STATIC_FOLDER = os.path.dirname(os.path.abspath(__file__))+'\\..\\static'
MODELS_FOLDER = os.path.dirname(os.path.abspath(__file__))+'\\..\\models'
DEBUG_ACTIVE = True
USE_RELOADER = True


# Database settings
DB_NAME = 'database.db'
MODEL_ID_LENTGH = 32
MODEL_NAME_MAX_LENTGH = 100
TEXTURE_ID_LENGTH = 32
REQUESTER_ID_MAX_LENGTH = 100
VALID_IMG_EXTENSIONS = ['jpg', 'png', 'jpeg']