import os

# APP settings
HOST = 'localhost'
PORT = 5000
DEBUG_ACTIVE = True
USE_RELOADER = True | DEBUG_ACTIVE # If the app is in debug mode, the reloader is automatically activated
USE_CORS = True
MODELS_FOLDER = './website/models/'

# Database settings
DB_NAME = 'database.db'
MODEL_ID_LENTGH = 32
TEXTURE_ID_LENGTH = 32
MODEL_NAME_MAX_LENTGH = 100
NUMBER_OF_ELEMENTS_IN_MODEL_TABLE = 14

# Static files settings
VALID_MODEL_EXTENSIONS = ['obj']
VALID_TEXTURE_EXTENSIONS = ['jpg', 'png', 'jpeg']
VALID_MODEL_TEXTURE_PREVIEW_EXTENSIONS = ['jpg', 'png', 'jpeg']
MAX_MODEL_SIZE = 10000000 # 10MB
MAX_IMG_SIZE = 10000000 # 10MB
MAX_FILE_UPLOAD_SIZE = max(MAX_MODEL_SIZE, MAX_IMG_SIZE)

# Server implementation
MODEL_FILE_NAME = 'model'
MODEL_TEXTURE_PREVIEW_NAME = 'preview'
MODEL_TEXTURE_PREVIEW_FORMAT = 'jpg'
TEXTURE_COLOR_IMG_SIZE = 300
TEXTURE_COLOR_IMG_FORMAT = 'png'