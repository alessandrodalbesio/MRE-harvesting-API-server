# APP settings
MODELS_FOLDER = '/var/www/models'

# Database settings
DB_NAME = 'database.db'
MODEL_ID_LENGTH = 32
TEXTURE_ID_LENGTH = 32
MODEL_NAME_MAX_LENGTH = 100

# Static files settings
VALID_MODEL_EXTENSIONS = ['obj']
VALID_TEXTURE_EXTENSIONS = ['jpg', 'png', 'jpeg']
VALID_MODEL_TEXTURE_PREVIEW_EXTENSIONS = ['jpg', 'png', 'jpeg']
MAX_MODEL_SIZE = 10000000 # 10MB
MAX_IMG_SIZE = 10000000 # 10MB

# Server implementation
MODEL_FILE_NAME = 'model'
MODEL_TEXTURE_PREVIEW_NAME = 'preview'
MODEL_TEXTURE_PREVIEW_FORMAT = 'jpg'
TEXTURE_COLOR_IMG_SIZE = 300 # px
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

# Settings for testings (not used in production)
PORT = 9000
HOST = '127.0.0.1'
DEBUG = True