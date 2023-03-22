import modules.db as db
from modules.errors import *
from modules.settings import *
import os
import shutil
import traceback

## Data retrieval ##

def getData():
    data = db.getAllData()
    finalData = []
    for elem in data:
        finalData.append({
            'id': elem.id,
            'name': elem.name,
            'imgSrc': 'assets/img/'+elem.id+'/img.jpg',
            'textures': [
                {
                    'id': texture.id,
                    'imgSrc': 'assets/img/'+elem.id+'/'+texture.id+'.jpg'
                }
                for texture in elem.textures
            ]
        })
    return finalData

## Data creation ##

def areCameraInfoValid(cameraInfo):
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
        if index not in cameraInfo:
            return False
    return True

def isColorValid(color):
    if len(color) != 7:
        return False
    if color[0] != '#':
        return False
    for i in range(1, 7):
        if color[i] not in '0123456789abcdef':
            return False
    return True


def createModel(modelName, modelOBJ, cameraInfo):
    # Validate the inputs
    if not areCameraInfoValid(cameraInfo):
        raise InputException("Invalid camera info")
    if modelOBJ.filename == '' or modelOBJ.filename.split('.')[-1] != 'obj':
        raise InputException("Invalid model file")
    if db.modelNameExists(modelName):
        raise InputException("Model name already exists")
    if len(modelName) == 0 or len(modelName) > MODEL_NAME_MAX_LENTGH:
        raise InputException("Invalid model name")

    # Manage the model creation
    modelID = db.generateModelID()
    try:
        # If it doesn't exist, create the models folder
        if not os.path.exists(MODELS_FOLDER):
            os.mkdir(MODELS_FOLDER)
        # Create the model folder
        os.mkdir(os.path.join(MODELS_FOLDER, modelID))
        modelOBJ.save(os.path.join(MODELS_FOLDER, modelID, 'model.obj'))
        db.createModel(modelID, modelName, cameraInfo, skipValidation=True)
    except Exception as err:
        # If something went wrong, rollback
        if os.path.exists(os.path.join(MODELS_FOLDER, modelID)):
            shutil.rmtree(os.path.join(MODELS_FOLDER, modelID), ignore_errors=True)
        if os.path.exists(os.path.join(MODELS_FOLDER, modelID, 'model.obj')):
            shutil.rmtree(os.path.join(MODELS_FOLDER, modelID, 'model.obj'), ignore_errors=True)
        db.deleteModel(modelID, skipValidation=True)
        raise SystemException('Something went wrong while creating the model', tracebackError=traceback.format_exc())
    else:
        return modelID


def createTextureByColor(modelID, color, cameraPhoto):
    if not db.modelIDExists(modelID):
        raise InputException("Invalid model ID")
    if not isColorValid(color):
        raise InputException("Invalid color")

    # Manage the texture creation
    textureID = db.generateTextureID()
    try:
        # Save the cameraPhoto
        cameraPhoto.save(os.path.join(MODELS_FOLDER, modelID, textureID+'-preview.jpg'))
        db.createTexture(modelID, textureID, skipValidation=True)
    except Exception as err:
        # If something went wrong, rollback
        db.deleteTexture(textureID, skipValidation=True)
        raise SystemException('Something went wrong while creating the texture', tracebackError=traceback.format_exc())
    else:
        return textureID


def createTextureByImage(modelID, IMG, cameraPhoto):
    if not db.modelIDIsValid(modelID):
        raise InputException("Model ID is not valid")
    if not db.modelIDExists(modelID):
        raise InputException("Model ID does not exists")
    if IMG.filename == '' or IMG.filename.split('.')[-1] not in VALID_IMG_EXTENSIONS:
        raise InputException("Invalid image file")
    if cameraPhoto.filename == '' or cameraPhoto.filename.split('.')[-1] not in VALID_IMG_EXTENSIONS:
        raise InputException("Invalid image file")
    
    # Manage the texture creation
    textureID = db.generateTextureID()
    try:
        IMG.save(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, textureID+'-texture.jpg'))
        cameraPhoto.save(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, textureID+'-preview.jpg'))
        db.createTexture(modelID, textureID, skipValidation=True)
    except Exception as err:
        # If something went wrong, rollback
        if os.path.exists(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, textureID+'-texture.jpg')):
            shutil.rmtree(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, textureID+'-texture.jpg'), ignore_errors=True)
        if os.path.exists(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, textureID+'-preview.jpg')):
            shutil.rmtree(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, textureID+'-preview.jpg'), ignore_errors=True)
        db.deleteTexture(modelID, textureID, skipValidation=True)
        raise SystemException('Something went wrong while creating the texture', tracebackError=traceback.format_exc())
    else:
        return textureID


"""
def modifyModelName(modelID, modelName):
    # Input verification
    if not db.modelIDIsValid(modelID):
        return errorHandler("Model ID is not valid", "INPUT_EXCEPTION")
    if not db.modelIDExists(modelID):
        return errorHandler("Model ID does not exists", "INPUT_EXCEPTION")
    if not db.modelNameIsValid(modelName):
        return errorHandler("Model name is not valid", "INPUT_EXCEPTION")
    if db.modelNameExists(modelName):
        return errorHandler("Model name already exists", "INPUT_EXCEPTION")
    
    # Manage the model name modification
    return db.updateModel(modelID, modelName)

def deleteModel(modelID):
    # Input verification
    if not db.modelIDIsValid(modelID):
        return errorHandler("Model ID is not valid", "INPUT_EXCEPTION")
    if not db.modelIDExists(modelID):
        return errorHandler("Model ID does not exists", "INPUT_EXCEPTION")
    
    # Manage the model deletion
    shutil.rmtree(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID))
    return db.deleteModel(modelID)


## Texture management ##

def createTexture(modelID, textureFile):
    # Input verification
    if not db.modelIDIsValid(modelID):
        return errorHandler("Model ID is not valid", "INPUT_EXCEPTION")
    if not db.modelIDExists(modelID):
        return errorHandler("Model ID does not exists", "INPUT_EXCEPTION")
    if textureFile.filename == '' or textureFile.filename.split('.')[-1] not in VALID_IMG_EXTENSIONS:
        return errorHandler("Invalid image file", "INPUT_EXCEPTION")
    
    # Manage the texture creation
    textureID = db.generateTextureID()
    textureFile.save(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, textureID+'.jpg'))
    return db.createTexture(modelID, textureID)

def deleteTexture(modelID, textureID):
    # Input verification
    if not db.modelIDIsValid(modelID):
        return errorHandler("Model ID is not valid", "INPUT_EXCEPTION")
    if not db.modelIDExists(modelID):
        return errorHandler("Model ID does not exists", "INPUT_EXCEPTION")
    if not db.textureIDIsValid(textureID):
        return errorHandler("Texture ID is not valid", "INPUT_EXCEPTION")
    if not db.textureIDExists(modelID, textureID):
        return errorHandler("Texture ID does not exists", "INPUT_EXCEPTION")
    
    # Manage the texture deletion
    os.remove(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, textureID+'.jpg'))
    return db.deleteTexture(modelID, textureID)


## Data from the system management ##

def setDataSystem():
    return errorHandler("Not implemented", "NOT_IMPLEMENTED")


## Generate data for the VR ##

def retrieveVRData():
    return errorHandler("Not implemented", "NOT_IMPLEMENTED")
"""