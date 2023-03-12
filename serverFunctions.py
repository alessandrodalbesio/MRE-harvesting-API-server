import dbManagement as db
from errorHandling import *
from settings import *
import os, shutil

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


## Model management ##

def createModel(modelName, modelOBJ, modelIMG):
    if not db.modelNameIsValid(modelName):
        return errorHandler("Model name is not valid", "INPUT_EXCEPTION")
    if db.modelNameExists(modelName):
        return errorHandler("Model name already exists", "INPUT_EXCEPTION")
    if modelOBJ.filename == '' or modelOBJ.filename.split('.')[-1] != 'obj':
        return errorHandler("Invalid model file", "INPUT_EXCEPTION")
    if modelIMG.filename == '' or modelIMG.filename.split('.')[-1] not in ['jpg', 'png', 'jpeg']:
        return errorHandler("Invalid image file", "INPUT_EXCEPTION")
        
    # Manage the model creation
    modelID = db.generateModelID()
    os.mkdir(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID))
    modelIMG.save(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, 'modelIMG.jpg'))
    modelOBJ.save(os.path.join(STATIC_FOLDER, MODELS_FOLDER, modelID, 'model.obj'))
    return db.createModel(modelID, modelName)

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
    if textureFile.filename == '' or textureFile.filename.split('.')[-1] not in ['jpg', 'png', 'jpeg']:
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