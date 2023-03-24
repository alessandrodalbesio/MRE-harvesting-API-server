import sqlite3, uuid, traceback
from modules.errors import *
from modules.settings import *
from modules.db.connection import *
from modules.db.models import *

#### Validation functions for textures ###
def generateTextureID():
    id = uniqueID()
    while textureIDExists(id):
        id = uniqueID()
    return id


def isTextureIDValid(textureID):
    return isinstance(textureID, str) and len(textureID) == TEXTURE_ID_LENGTH


def textureIDExists(textureID):
    isTextureIDValid(textureID)
    try:
        con, cur = connect()
        res = cur.execute("SELECT IDTexture FROM texture WHERE IDTexture = :textureID", {"textureID": textureID})
        numElement = len(res.fetchall())
        closeConnection(con)
        return numElement > 0
    except sqlite3.Error:
        raise SystemException("Something went wrong during the validation of the texture ID", traceback.format_exc())


### Data retrival functions ###

def getTexturesList(IDModel):
    try:
        con, cur = connect()
        res = cur.execute("SELECT IDTexture, isDefault FROM texture WHERE IDModel = :IDModel", {"IDModel": IDModel})
        textureList = res.fetchall()
        closeConnection(con)
        return textureList
    except sqlite3.Error:
        raise SystemException("Something went wrong during the retrieval of the textures list", traceback.format_exc())

def getTextureInfo(IDTexture):
    try:
        con, cur = connect()
        res = cur.execute("SELECT * FROM texture WHERE IDTexture = :IDTexture", {"IDTexture": IDTexture})
        textureInfo = res.fetchone()
        closeConnection(con)
        return textureInfo
    except sqlite3.Error:
        raise SystemException("Something went wrong during the retrieval of the texture info", traceback.format_exc())

def isTextureFromModel(newDefaultTexture, modelID):
    try:
        con, cur = connect()
        res = cur.execute("SELECT IDTexture FROM texture WHERE IDModel = :IDModel AND IDTexture = :IDTexture", {"IDModel": modelID, "IDTexture": newDefaultTexture})
        numElement = len(res.fetchall())
        closeConnection(con)
        return numElement > 0
    except sqlite3.Error:
        raise SystemException("Something went wrong during the validation of the texture ID", traceback.format_exc())

### Creation functions ###

def changeDefaultTexture(modelID, newDefaultTexture):
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

    # Change default texture
    try:
        con, cur = connect()
        cur.execute("UPDATE texture SET isDefault = 0 WHERE IDModel = :IDModel", {"IDModel": modelID})
        cur.execute("UPDATE texture SET isDefault = 1 WHERE IDTexture = :IDTexture", {"IDTexture": newDefaultTexture})
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the change of the default texture", traceback.format_exc())
    saveInfoLog(f"Default texture of the model {modelID} has been changed to {newDefaultTexture}")

def isColorValid(color):
    if len(color) != 7:
        return False
    if color[0] != '#':
        return False
    for i in range(1, 7):
        if color[i] not in '0123456789abcdef':
            return False
    return True

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
    if isColor and not isColorValid(colorHEX):
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

def deleteAllTexturesFromModel(modelID):
    # Validate input
    if not isModelIDValid(modelID):
        raise InputException("Model ID is not valid")

    # Delete textures
    try:
        con, cur = connect()
        cur.execute("DELETE FROM texture WHERE IDModel = :modelID", {"modelID": modelID})
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the deletion of the textures", traceback.format_exc())
    saveInfoLog(f"All textures of the model {modelID} have been deleted")

def deleteTexture(textureID):
    # Validate input
    if not isTextureIDValid(textureID):
        raise InputException("Texture ID is not valid")
    if not textureIDExists(textureID):
        raise InputException("Texture ID does not exist")

    # Delete texture
    try:
        con, cur = connect()
        cur.execute("DELETE FROM texture WHERE IDTexture = :textureID",
                    {"textureID": textureID})
        con.commit()
        closeConnection(con)
    except sqlite3.Error:
        raise SystemException("Something went wrong during the deletion of the texture", traceback.format_exc())
    saveInfoLog(f"Texture {textureID} has been deleted")