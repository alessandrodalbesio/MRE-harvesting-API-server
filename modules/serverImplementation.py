# Import all the needed global modules
import os, shutil, traceback
from PIL import Image 

# Import all the needed local modules
import modules.db.models as dbModels
import modules.db.textures as dbTextures
from modules.settings import *
from modules.errors import *
from modules.colors import *

## Data retrieval ##
def getModelsList():
    modelList = dbModels.getModelsList()
    returnList = []
    for model in modelList:
        print(model[0])
        textureList = dbTextures.getTexturesList(model[0])
        print(textureList)
        for texture in textureList:
            if texture[1] == 1:
                defaultTexture = texture[0]
                break
        returnList.append({
            'IDModel': model[0],
            'modelName': model[1],
            'defaultTexture': defaultTexture,
            'textures': [texture[0] for texture in textureList]
        })
    return returnList

def getModelInfoByID(IDModel):
    modelInfo = dbModels.getModelInfo(IDModel)
    texturesList = dbTextures.getTexturesList(IDModel)
    return {
        'IDModel': modelInfo[0],
        'modelName': modelInfo[1],
        'textures': [{'IDTexture': texture[0], 'isDefault': texture[1] == 1} for texture in texturesList]
    }

## Data update ##
def updateModelName(IDModel, newName):
    dbModels.updateModelName(IDModel, newName)

## Data deletion ##
def deleteModel(IDModel):
    dbTextures.deleteAllTexturesFromModel(IDModel)
    dbModels.deleteModel(IDModel)
    shutil.rmtree(os.path.join(MODELS_FOLDER, IDModel), ignore_errors=True)

## Data creation ##

def arePreviewInfoValid(previewInfo):
    requiredIndex = [
        'ambientLightInScene',
        'backgroundColor',
        'cameraPositionX',
        'cameraPositionY',
        'cameraPositionZ',
        'cameraRotationX',
        'cameraRotationY',
        'cameraRotationZ',
        'cameraZoom',  
        'groundColor', 
        'groundVisibility', 
        'shadows'
    ]
    for index in requiredIndex:
        if index not in previewInfo:
            return False
    return True

def fileSize(file):
    return 10

# MODEL CREATION #
def createModel(modelName, modelOBJ, previewInfo):
    try:
        if not arePreviewInfoValid(previewInfo):
            raise InputException("Invalid preview informations", previewInfo)
        if modelOBJ.filename == '':
            raise InputException("No model file")
        if modelOBJ.filename.split('.')[-1] not in VALID_MODEL_EXTENSIONS:
            raise InputException("Invalid model file", modelOBJ.filename.split('.')[-1])
        if dbModels.modelNameExists(modelName):
            raise InputException("Model name already exists", modelName)
        if len(modelName) == 0 or len(modelName) > MODEL_NAME_MAX_LENTGH:
            raise InputException("Invalid model name", len(modelName))
        if fileSize(modelOBJ) > MAX_MODEL_SIZE:
            raise InputException("Model file too big", fileSize(modelOBJ))
        if fileSize(modelOBJ) == 0:
            raise InputException("Model file is empty", fileSize(modelOBJ))

        # Manage the model creation
        modelID = dbModels.generateModelID()
        modelExtension = modelOBJ.filename.split('.')[-1]
        # If it doesn't exist, create the models folder
        if not os.path.exists(os.path.join(MODELS_FOLDER)):
            os.mkdir(MODELS_FOLDER)
        # Create the model folder
        os.mkdir(os.path.join(MODELS_FOLDER, modelID))
        # Save the model file
        modelOBJ.save(os.path.join(MODELS_FOLDER, modelID, SAVED_MODEL_NAME_FILE+'.'+modelExtension))
        # Save the model into the database
        dbModels.createModel(modelID, modelName, previewInfo, modelExtension)
    except InputException:
        raise
    except Exception as err:
        if os.path.exists(os.path.join(MODELS_FOLDER, modelID)):
            shutil.rmtree(os.path.join(MODELS_FOLDER, modelID), ignore_errors=True)
        if dbModels.modelIDExists(modelID):
            dbModels.deleteModel(modelID)
        raise SystemException('Something went wrong while creating the model', tracebackError=traceback.format_exc())
    else:
        return modelID

# TEXTURE CREATION #
def createTextureByColor(modelID, color, texturePreview, isNewModel = False):
    def rollback():
        if textureID != None:
            if os.path.exists(os.path.join(MODELS_FOLDER, modelID, textureID+'-'+PREVIEW_IMG_NAME_FILE+'.'+PREVIEW_IMG_FORMAT)):
                os.remove(os.path.join(MODELS_FOLDER, modelID, textureID+'-'+PREVIEW_IMG_NAME_FILE+'.'+PREVIEW_IMG_FORMAT))
            if os.path.exists(os.path.join(MODELS_FOLDER, modelID, textureID+'.'+DEFAULT_COLOR_IMG_FORMAT)):
                os.remove(os.path.join(MODELS_FOLDER, modelID, textureID+'.'+DEFAULT_COLOR_IMG_FORMAT))
            if dbTextures.textureIDExists(textureID):
                dbTextures.deleteTexture(textureID)
        if isNewModel:
            deleteModel(modelID)
    try:
        textureID = None

        if not dbModels.modelIDExists(modelID):
            raise InputException("Invalid model ID", modelID)
        if not isColorValidHEX(color):
            raise InputException("Invalid color", color)
        if not isinstance(isNewModel, bool):
            raise InputException("Invalid isNewModel value", isNewModel)
        if texturePreview.filename == '':
            raise InputException("No texture preview file")
        if texturePreview.filename.split('.')[-1] not in VALID_IMG_EXTENSIONS:
            raise InputException("Invalid texture preview file", texturePreview.filename.split('.')[-1])
        if fileSize(texturePreview) > MAX_IMG_SIZE:
            raise InputException("Texture preview file too big", fileSize(texturePreview))
        if fileSize(texturePreview) == 0:
            raise InputException("Texture preview file is empty", fileSize(texturePreview))

        # Manage the texture creation
        textureID = dbTextures.generateTextureID()
        # Save the texture preview
        texturePreview.save(os.path.join(MODELS_FOLDER, modelID, textureID+'-'+PREVIEW_IMG_NAME_FILE+'.'+PREVIEW_IMG_FORMAT))
        # Save the texture on the database
        dbTextures.createTexture(textureID, modelID, DEFAULT_COLOR_IMG_FORMAT,isNewModel=isNewModel, isColor=True, colorHEX=color)
        # Create the texture image and save it on the server (used only for the texture selection)
        im = Image.new(mode="RGB", size=(PREVIEW_IMG_SIZE, PREVIEW_IMG_SIZE), color=convertHexColorToRGB(color))
        im.save(os.path.join(MODELS_FOLDER, modelID, textureID+'.'+DEFAULT_COLOR_IMG_FORMAT))
    except InputException:
        rollback()
        raise
    except SystemException:
        rollback()
        raise
    except Exception:
        rollback()
        raise SystemException('Something went wrong while creating the texture', tracebackError=traceback.format_exc())
    else:
        return textureID


def createTextureByImage(modelID, IMG, texturePreview, isNewModel = False):
    def rollback():
        if textureID != None and extension != None:
            if os.path.exists(os.path.join(MODELS_FOLDER, modelID, textureID+'-'+PREVIEW_IMG_NAME_FILE+'.'+PREVIEW_IMG_FORMAT)):
                os.remove(os.path.join(MODELS_FOLDER, modelID, textureID+'-'+PREVIEW_IMG_NAME_FILE+'.'+PREVIEW_IMG_FORMAT))
            if os.path.exists(os.path.join(MODELS_FOLDER, modelID, textureID+'.'+extension)):
                os.remove(os.path.join(MODELS_FOLDER, modelID, textureID+'.'+extension))
            if dbTextures.textureIDExists(textureID):
                dbTextures.deleteTexture(textureID)
        if isNewModel:
            deleteModel(modelID)
    try:
        textureID = extension = None

        if not dbModels.modelIDExists(modelID):
            raise InputException("Invalid model ID", modelID)
        if IMG.filename == '':
            raise InputException("No texture file")
        if IMG.filename.split('.')[-1] not in VALID_IMG_EXTENSIONS:
            raise InputException("Invalid texture file", IMG.filename.split('.')[-1])
        if not isinstance(isNewModel, bool):
            raise InputException("Invalid isNewModel value", isNewModel)
        if texturePreview.filename == '':
            raise InputException("No texture preview file")
        if texturePreview.filename.split('.')[-1] not in VALID_IMG_EXTENSIONS:
            raise InputException("Invalid texture preview file", texturePreview.filename.split('.')[-1])
        if fileSize(IMG) > MAX_IMG_SIZE:
            raise InputException("Texture file too big", fileSize(IMG))
        if fileSize(texturePreview) > MAX_IMG_SIZE:
            raise InputException("Texture preview file too big", fileSize(texturePreview))
        if fileSize(IMG) == 0:
            raise InputException("Texture file is empty", fileSize(IMG))
        if fileSize(texturePreview) == 0:
            raise InputException("Texture preview file is empty", fileSize(texturePreview))

        # Manage the texture creation
        textureID = dbTextures.generateTextureID()
        extension = IMG.filename.split('.')[-1]
        # Save the texture preview
        texturePreview.save(os.path.join(MODELS_FOLDER, modelID, textureID+'-'+PREVIEW_IMG_NAME_FILE+'.'+PREVIEW_IMG_FORMAT))
        # Save the texture on the database
        dbTextures.createTexture(textureID, modelID, extension, isNewModel=isNewModel, isColor=False, isImage = True)
        # Save the texture on the server
        IMG.save(os.path.join(MODELS_FOLDER, modelID, textureID+'.'+extension))
    except InputException:
        rollback()
        raise
    except SystemException:
        rollback()
        raise
    except Exception:
        rollback()
        raise SystemException('Something went wrong while creating the texture', tracebackError=traceback.format_exc())
    else:
        return textureID