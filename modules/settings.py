import os

# APP settings
HOST = 'localhost'
PORT = 5000
DEBUG_ACTIVE = True
USE_RELOADER = True | DEBUG_ACTIVE # If the app is in debug mode, the reloader is automatically activated
MODELS_FOLDER = './website/models/'
# If the folder doesn't exist, create it
if not os.path.exists(MODELS_FOLDER):
    os.mkdir(MODELS_FOLDER)



# Database settings
DB_NAME = 'database.db'
MODEL_ID_LENTGH = 32
MODEL_NAME_MAX_LENTGH = 100
TEXTURE_ID_LENGTH = 32


# Static files settings
VALID_IMG_EXTENSIONS = ['jpg', 'png', 'jpeg']
VALID_MODEL_EXTENSIONS = ['obj']
MAX_MODEL_SIZE = 10000000 # 10MB
MAX_IMG_SIZE = 10000000 # 10MB

# Server implementation
SAVED_MODEL_NAME_FILE = 'model'
PREVIEW_IMG_NAME_FILE = 'preview'
PREVIEW_IMG_SIZE = 300
PREVIEW_IMG_FORMAT = 'jpg'
DEFAULT_COLOR_IMG_FORMAT = 'png'