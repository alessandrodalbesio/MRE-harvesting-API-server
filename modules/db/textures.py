import sqlite3, traceback
from modules.errors import *
from modules.settings import *
from modules.db.connection import *
from modules.db.models import *
from modules.colors import *

#### Validation functions for textures ###
def generateTextureID():
    id = uniqueID()
    while textureIDExists(id):
        id = uniqueID()
    return id


def isTextureIDValid(textureID):
    return isinstance(textureID, str) and len(textureID) == TEXTURE_ID_LENGTH


def textureIDExists(textureID):
    try:
        if not isTextureIDValid(textureID):
            raise InputException("Invalid texture ID")
        con, cur = connect()
        res = cur.execute("SELECT IDTexture FROM texture WHERE IDTexture = :textureID", {"textureID": textureID})
        numElement = len(res.fetchall())
        closeConnection(con)
        return numElement > 0
    except sqlite3.Error:
        raise SystemException("Something went wrong during the validation of the texture ID", traceback.format_exc())


### Data retrival functions ###

def getTextureInformationFromDatabase(textureDatabaseData):
    return {
        'IDTexture': textureDatabaseData[0],
        'IDModel': textureDatabaseData[1],
        'isDefault': textureDatabaseData[2],
        'isColor': textureDatabaseData[3],
        'colorHex': textureDatabaseData[4],
        'isImage': textureDatabaseData[5],
        'extension': textureDatabaseData[6]
    }


def getTexturesList(IDModel):
    try:
        if not isModelIDValid(IDModel):
            raise InputException("Invalid model ID")
        if not modelIDExists(IDModel):
            raise InputException("Model ID does not exist")
        con, cur = connect()
        res = cur.execute("SELECT * FROM texture WHERE IDModel = :IDModel", {"IDModel": IDModel})
        textureList = res.fetchall()
        closeConnection(con)
        for i in range(len(textureList)):
            textureList[i] = getTextureInformationFromDatabase(textureList[i])
        return textureList
    except sqlite3.Error:
        raise SystemException("Something went wrong during the retrieval of the textures list", traceback.format_exc())

def getTextureInfo(IDTexture):
    try:
        if not isTextureIDValid(IDTexture):
            raise InputException("Invalid texture ID")
        if not textureIDExists(IDTexture):
            raise InputException("Texture ID does not exist")
        con, cur = connect()
        res = cur.execute("SELECT * FROM texture WHERE IDTexture = :IDTexture", {"IDTexture": IDTexture})
        textureInfo = res.fetchone()
        closeConnection(con)
        textureInfo = getTextureInformationFromDatabase(textureInfo)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the retrieval of the texture info", traceback.format_exc())

def isTextureFromModel(newDefaultTexture, modelID):
    try:
        if not isTextureIDValid(newDefaultTexture):
            raise InputException("Invalid texture ID")
        if not isModelIDValid(modelID):
            raise InputException("Invalid model ID")
        if not textureIDExists(newDefaultTexture):
            raise InputException("Texture ID does not exist")
        if not modelIDExists(modelID):
            raise InputException("Model ID does not exist")
        con, cur = connect()
        res = cur.execute("SELECT IDTexture FROM texture WHERE IDModel = :IDModel AND IDTexture = :IDTexture", {"IDModel": modelID, "IDTexture": newDefaultTexture})
        numElement = len(res.fetchall())
        closeConnection(con)
        return numElement > 0
    except sqlite3.Error:
        raise SystemException("Something went wrong during the validation of the texture ID", traceback.format_exc())

### Creation functions ###

def changeDefaultTexture(modelID, newDefaultTexture):
    # Change default texture
    try:
        # Validate input
        if not isModelIDValid(modelID):
            raise InputException("Model ID is not valid")
        if not isTextureIDValid(newDefaultTexture):
            raise InputException("Texture ID is not valid")
        if not modelIDExists(modelID):
            raise InputException("Model ID does not exist")
        if not textureIDExists(newDefaultTexture):
            raise InputException("Texture ID does not exist")
        if not isTextureFromModel(newDefaultTexture, modelID):
            raise InputException("Texture ID does not belong to the model")
        con, cur = connect()
        cur.execute("UPDATE texture SET isDefault = 0 WHERE IDModel = :IDModel", {"IDModel": modelID})
        cur.execute("UPDATE texture SET isDefault = 1 WHERE IDTexture = :IDTexture", {"IDTexture": newDefaultTexture})
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the change of the default texture", traceback.format_exc())
    saveInfoLog(f"Default texture of the model {modelID} has been changed to {newDefaultTexture}")

def createTexture(textureID, modelID, extension, isNewModel=False, isColor=False, colorHEX=None, isImage=False):
    # Validate input
    if not isTextureIDValid(textureID):
        raise InputException("Texture ID is not valid", textureID)
    if not isModelIDValid(modelID):
        raise InputException("Model ID is not valid", modelID)
    if textureIDExists(textureID):
        raise InputException("Texture ID already exists", textureID)
    if not modelIDExists(modelID):
        raise InputException("Model ID does not exist", modelID)
    if not isinstance(isNewModel, bool):
        raise InputException("isDefault is not a boolean", isNewModel)
    if not isinstance(isColor, bool):
        raise InputException("isColor is not a boolean", isColor)
    if not isinstance(isImage, bool):
        raise InputException("isImage is not a boolean", isImage)
    if isColor and colorHEX is None:
        raise InputException("Color HEX is not defined", colorHEX)
    if isColor and not isinstance(colorHEX, str):
        raise InputException("Color HEX is not a string", colorHEX)
    if isColor and not isColorValidHEX(colorHEX):
        raise InputException("Color HEX is not valid", colorHEX)
    if isImage and colorHEX is not None:
        raise InputException("Color HEX is defined but isImage is true", colorHEX)
    if not isColor and not isImage:
        raise InputException("isColor and isImage are both false")
    if isColor and isImage:
        raise InputException("isColor and isImage are both true")
    
    # Create texture
    try:
        con, cur = connect()
        cur.execute("""
            INSERT INTO texture VALUES (
                :textureID, 
                :modelID, 
                :isDefault,
                :isColor,
                :colorHEX,
                :isImage,
                :extension)""", 
            {
                "textureID": textureID, 
                "modelID": modelID, 
                "isDefault": isNewModel, 
                "isColor": isColor, 
                "colorHEX": colorHEX, 
                "isImage": isImage,
                "extension": extension
            }
        )
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        deleteModel(modelID)
        raise SystemException("Something went wrong during the creation of the texture", traceback.format_exc())
    
    saveInfoLog(f"Texture {textureID} has been created")

### Delete functions ###

def deleteAllTexturesFromModel(modelID, requireModelExists=False):
    # Delete textures
    try:
        if not isModelIDValid(modelID):
            raise InputException("Model ID is not valid")
        if requireModelExists and not modelIDExists(modelID):
            raise InputException("Model ID does not exist")
        con, cur = connect()
        cur.execute("DELETE FROM texture WHERE IDModel = :modelID", {"modelID": modelID})
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the deletion of the textures", traceback.format_exc())
    saveInfoLog(f"All textures of the model {modelID} have been deleted")

def deleteTexture(textureID):
    # Delete texture
    try:
        if not isTextureIDValid(textureID):
            raise InputException("Texture ID is not valid")
        if not textureIDExists(textureID):
            raise InputException("Texture ID does not exist")
        con, cur = connect()
        cur.execute("DELETE FROM texture WHERE IDTexture = :textureID",
                    {"textureID": textureID})
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the deletion of the texture", traceback.format_exc())
    saveInfoLog(f"Texture {textureID} has been deleted")