import os

# APP settings
MODELS_FOLDER = '/var/www/models'
WEBSOCKET_API_URL = 'http://virtualenv.epfl.ch/ws/endpoints/'

# Database settings
DB_NAME = 'database.db'
MODEL_ID_LENGTH = 32
TEXTURE_ID_LENGTH = 32
MODEL_NAME_MAX_LENGTH = 100
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

# Settings dictionary
SETTINGS_ALL = {
    'modelIDLength': MODEL_ID_LENGTH,
    'textureIDLength': TEXTURE_ID_LENGTH,
    'maxModelNameLength': MODEL_NAME_MAX_LENGTH,
    'validModelExtensions': VALID_MODEL_EXTENSIONS,
    'validTextureExtensions': VALID_TEXTURE_EXTENSIONS,
    'modelFileName': MODEL_FILE_NAME,
    'modelTexturePreviewName': MODEL_TEXTURE_PREVIEW_NAME,
    'modelTexturePreviewFormat': MODEL_TEXTURE_PREVIEW_FORMAT,
    'maxModelFileSize': MAX_MODEL_SIZE,
    'maxTextureFileSize': MAX_IMG_SIZE,
}