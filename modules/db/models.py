import sqlite3, traceback
from modules.errors import *
from modules.settings import *
from modules.db.connection import *
from modules.db.models import *


def getCameraInfoInDictionary(cameraInfoSQL):
    if not isinstance(cameraInfoSQL, tuple) and len(cameraInfoSQL) != 12:
        raise InputException("The camera info SQL is not valid")
    return {
            'ambientLightInScene': cameraInfoSQL[10],
            'backgroundColor': cameraInfoSQL[9],
            'cameraPositionX': cameraInfoSQL[0],
            'cameraPositionY': cameraInfoSQL[1],
            'cameraPositionZ': cameraInfoSQL[2],
            'cameraRotationX': cameraInfoSQL[3],
            'cameraRotationY': cameraInfoSQL[4],
            'cameraRotationZ': cameraInfoSQL[5],
            'cameraZoom': cameraInfoSQL[6],
            'groundColor': cameraInfoSQL[7],
            'groundVisibility': cameraInfoSQL[8],
            'shadows': cameraInfoSQL[11]
        }

## Data validation functions ##
def generateModelID():
    generatedID = uniqueID()
    while modelIDExists(generatedID):
        generatedID = uniqueID()
    return generatedID

def isModelIDValid(modelID):
    return isinstance(modelID, str) and len(modelID) == MODEL_ID_LENGTH

def modelIDExists(modelID):
    try:
        isModelIDValid(modelID)
        con, cur = connect()
        res = cur.execute("SELECT IDModel FROM model WHERE IDModel = :modelID", {"modelID": modelID})
        numElement = len(res.fetchall())
        closeConnection(con)
        return numElement > 0
    except sqlite3.Error:
        raise SystemException("Something went wrong during the validation of the model ID", traceback.format_exc())

def isModelNameValid(modelName):
    return isinstance(modelName, str) and 0 < len(modelName) <= MODEL_NAME_MAX_LENGTH

def modelNameExists(modelName):
    try:
        isModelNameValid(modelName)
        con, cur = connect()
        res = cur.execute("SELECT IDModel FROM model WHERE nameModel = :modelName", {"modelName": modelName})
        numElement = len(res.fetchall())
        closeConnection(con)
        return numElement > 0
    except sqlite3.Error:
        raise SystemException("Something went wrong during the validation of the model name", traceback.format_exc())


## Data retrivial functions ##
def getModelsList():
    try:
        con, cur = connect()
        res = cur.execute("SELECT * FROM model")
        modelList = res.fetchall()
        closeConnection(con)
        return modelList
    except sqlite3.Error:
        raise SystemException("Something went wrong during the retrival of the models list", traceback.format_exc())
    
def getModelInfo(IDModel):
    # Validate input
    if not isModelIDValid(IDModel):
        raise InputException("Model ID is not valid", IDModel)
    if not modelIDExists(IDModel):
        raise InputException("Model ID does not exist", IDModel)
    try:
        con, cur = connect()
        res = cur.execute("SELECT * FROM model WHERE IDModel = :IDModel", {"IDModel": IDModel})
        modelInfo = res.fetchone()
        closeConnection(con)
        return modelInfo
    except sqlite3.Error:
        raise SystemException("Something went wrong during the retrival of the model info", traceback.format_exc())

def getModelInfoByName(modelName):
    # Validate input
    if not isModelNameValid(modelName):
        raise InputException("Model name is not valid", modelName)
    if not modelNameExists(modelName):
        raise InputException("Model name does not exist", modelName)
    try:
        con, cur = connect()
        res = cur.execute("SELECT * FROM model WHERE nameModel = :modelName", {"modelName": modelName})
        modelInfo = res.fetchone()
        closeConnection(con)
        return modelInfo
    except sqlite3.Error:
        raise SystemException("Something went wrong during the retrival of the model info", traceback.format_exc())


## Creation functions ##
def createModel(modelID, modelName, cameraInfo, modelExtension):
    # Validate input
    if not isModelIDValid(modelID):
        raise InputException("Model ID is not valid")
    if not isModelNameValid(modelName):
        raise InputException("Model name is not valid")
    if modelIDExists(modelID):
        raise InputException("Model ID already exists")
    if modelNameExists(modelName):
        raise InputException("Model name already exists")

    # Create model
    try:
        con, cur = connect()
        cur.execute(f"""INSERT INTO 'model' VALUES(
            :IDModel,
            :nameModel,
            :cameraPositionX,
            :cameraPositionY,
            :cameraPositionZ,
            :cameraRotationX,
            :cameraRotationY,
            :cameraRotationZ,
            :cameraZoom,
            :groundColorHex,
            :groundVisibility,
            :backgroundColorHex,
            :ambientLightInScene,
            :shadows,
            :modelExtension
            )
        """, {
            "IDModel": modelID,
            "nameModel": modelName,
            "cameraPositionX": cameraInfo["cameraPositionX"],
            "cameraPositionY": cameraInfo["cameraPositionY"],
            "cameraPositionZ": cameraInfo["cameraPositionZ"],
            "cameraRotationX": cameraInfo["cameraRotationX"],
            "cameraRotationY": cameraInfo["cameraRotationY"],
            "cameraRotationZ": cameraInfo["cameraRotationZ"],
            "cameraZoom": cameraInfo["cameraZoom"],
            "groundColorHex": cameraInfo["groundColor"],
            "groundVisibility": cameraInfo["groundVisibility"],
            "backgroundColorHex": cameraInfo["backgroundColor"],
            "ambientLightInScene": cameraInfo["ambientLightInScene"],
            "shadows": cameraInfo["shadows"],
            "modelExtension": modelExtension
        })
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the creation of the model", traceback.format_exc())
    
    saveInfoLog(f"Model {modelName} with the id {modelID} has been created")


## Update functions ##
def updateModel(IDModel, newName):
    # Validate input
    if not isModelIDValid(IDModel):
        raise InputException("Model ID is not valid")
    if not isModelNameValid(newName):
        raise InputException("Model name is not valid")
    if not modelIDExists(IDModel):
        raise InputException("Model ID does not exist")
    if modelNameExists(newName):
        raise InputException("Model name already exists")

    # Update model
    try:
        con, cur = connect()
        cur.execute(f"""UPDATE model SET nameModel = :newName WHERE IDModel = :IDModel""", {
            "newName": newName,
            "IDModel": IDModel
        })
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the update of the model", traceback.format_exc())
    
    saveInfoLog(f"Model {IDModel} has been updated with the name {newName}")

def updateModelName(modelID, newNameModel):
    # Validate input
    if not isModelIDValid(modelID):
        raise InputException("Model ID is not valid")
    if not isModelNameValid(newNameModel):
        raise InputException("Model name is not valid")
    if not modelIDExists(modelID):
        raise InputException("Model ID does not exist")
    if modelNameExists(newNameModel):
        raise InputException("Model name already exists")

    # Update model
    try:
        con, cur = connect()
        cur.execute(f"""UPDATE model SET nameModel = :newNameModel WHERE IDModel = :modelID""", {
            "newNameModel": newNameModel,
            "modelID": modelID
        })
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the update of the model", traceback.format_exc())
    
    saveInfoLog(f"Model {modelID} has been updated with the name {newNameModel}")

## Delete functions ##
def deleteModel(modelID):
    # Validate input
    if not isModelIDValid(modelID):
        raise InputException("Model ID is not valid")
    if not modelIDExists(modelID):
        raise InputException("Model ID does not exist")

    # Delete model
    try:
        con, cur = connect()
        cur.execute("DELETE FROM model WHERE IDModel = :modelID", {"modelID": modelID})
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the deletion of the model", traceback.format_exc())
    
    saveInfoLog(f"Model {modelID} has been deleted")