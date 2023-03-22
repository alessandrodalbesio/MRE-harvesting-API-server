import sqlite3
import uuid
from modules.errors import *
from modules.settings import *

### Global functions definition ###


def connect():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS 'model' (
        'IDModel' CHAR({MODEL_ID_LENTGH}) NOT NULL PRIMARY KEY,
        'nameModel' VARCHAR({MODEL_NAME_MAX_LENTGH}) NOT NULL UNIQUE,
        'cameraPositionX' FLOAT NOT NULL,
        'cameraPositionY' FLOAT NOT NULL,
        'cameraPositionZ' FLOAT NOT NULL,
        'cameraRotationX' FLOAT NOT NULL,
        'cameraRotationY' FLOAT NOT NULL,
        'cameraRotationZ' FLOAT NOT NULL,
        'cameraZoom' FLOAT NOT NULL,
        'groundColorHex' CHAR(7) NOT NULL,
        'groundVisibility' BOOLEAN NOT NULL,
        'backgroundColorHex' CHAR(7) NOT NULL,
        'ambientLightInScene' BOOLEAN NOT NULL,
        'shadows' BOOLEAN NOT NULL
    )""")
    cur.execute(f"""CREATE TABLE IF NOT EXISTS 'texture' (
        'IDTexture' CHAR({TEXTURE_ID_LENGTH}) PRIMARY KEY, 
        'IDModel' CHAR({MODEL_ID_LENTGH}) NOT NULL, 
        FOREIGN KEY ('IDModel') REFERENCES model('IDModel')
    )""")
    return con, cur


def closeConnection(con):
    con.close()


def uniqueID():
    return str(uuid.uuid4().hex)


### Validation functions ###
def generateModelID():
    id = uniqueID()
    while modelIDExists(id):
        id = uniqueID()
    return id


def isModelIDValid(modelID):
    return isinstance(modelID, str) and len(modelID) == MODEL_ID_LENTGH


def modelIDExists(modelID):
    isModelIDValid(modelID)
    con, cur = connect()
    res = cur.execute("SELECT IDModel FROM model WHERE IDModel = :modelID", {
                      "modelID": modelID})
    numElement = len(res.fetchall())
    closeConnection(con)
    return numElement > 0


def isModelNameValid(modelName):
    return isinstance(modelName, str) and 0 < len(modelName) <= MODEL_NAME_MAX_LENTGH


def modelNameExists(modelName):
    isModelNameValid(modelName)
    con, cur = connect()
    res = cur.execute("SELECT IDModel FROM model WHERE nameModel = :modelName", {
                      "modelName": modelName})
    numElement = len(res.fetchall())
    closeConnection(con)
    return numElement > 0


def generateTextureID():
    id = uniqueID()
    while textureIDExists(id):
        id = uniqueID()
    return id


def isTextureIDValid(textureID):
    return isinstance(textureID, str) and len(textureID) == TEXTURE_ID_LENGTH


def textureIDExists(textureID):
    isTextureIDValid(textureID)
    con, cur = connect()
    res = cur.execute("SELECT IDTexture FROM texture WHERE IDTexture = :textureID", {
                      "textureID": textureID})
    numElement = len(res.fetchall())
    closeConnection(con)
    return numElement > 0


### Creation functions ###
def createModel(modelID, modelName, cameraInfo, skipValidation=False):
    # Validate input
    if not skipValidation and not isModelIDValid(modelID):
        raise InputException("Model ID is not valid")
    if not skipValidation and not isModelNameValid(modelName):
        raise InputException("Model name is not valid")
    if not skipValidation and modelIDExists(modelID):
        raise InputException("Model ID already exists")
    if not skipValidation and modelNameExists(modelName):
        raise InputException("Model name already exists")

    # Create model
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
        :shadows
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
        "shadows": cameraInfo["shadows"]
    })
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Model {modelName} with the id {modelID} has been created")


def createTexture(textureID, modelID, skipValidation=False):
    # Validate input
    if not skipValidation and not isTextureIDValid(textureID):
        raise InputException("Texture ID is not valid")
    if not skipValidation and not isModelIDValid(modelID):
        raise InputException("Model ID is not valid")
    if not skipValidation and not modelIDExists(modelID):
        raise InputException("Model ID does not exist")
    if not skipValidation and textureIDExists(textureID):
        raise InputException("Texture ID already exists")

    # Create texture
    con, cur = connect()
    cur.execute("INSERT INTO texture VALUES (:textureID, :modelID)", {
                "textureID": textureID, "modelID": modelID})
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Texture {textureID} has been created")


### Delete functions ###
def deleteModel(modelID, skipValidation=False):
    # Validate input
    if not skipValidation and not isModelIDValid(modelID):
        raise InputException("Model ID is not valid")
    if not skipValidation and not modelIDExists(modelID):
        raise InputException("Model ID does not exist")

    # Delete model
    con, cur = connect()
    cur.execute("DELETE FROM model WHERE IDModel = :modelID", {"modelID": modelID})
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Model {modelID} has been deleted")


def deleteTexture(textureID, skipValidation=False):
    # Validate input
    if not skipValidation and not isTextureIDValid(textureID):
        raise InputException("Texture ID is not valid")
    if not skipValidation and not textureIDExists(textureID):
        raise InputException("Texture ID does not exist")

    # Delete texture
    con, cur = connect()
    cur.execute("DELETE FROM texture WHERE IDTexture = :textureID",
                {"textureID": textureID})
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Texture {textureID} has been deleted")


"""

def getAllData():
    con, cur = connect()
    data = cur.execute("SELECT id, name FROM model")
    data = [
        {
            "id": model[0],
            "name": model[1],
            "textures": [texture[0] for texture in cur.execute("SELECT id FROM texture WHERE idModel = :idModel", {"idModel": model[0]})]
        } for model in data
    ]
    closeConnection(con)
    return data


### Models management ###

# Model management functions #
def createModel(modelID, modelName):
    con, cur = connect()
    cur.execute("INSERT INTO model VALUES (:modelID, :modelName)", {"modelID": modelID, "modelName": modelName})
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Model {modelName} with the id {id} has been created")
    return Response("Model created", 200)

def updateModel(modelID, newModelname):
    con, cur = connect()
    cur.execute("UPDATE model SET name = :modelName WHERE id = :modelID", {"modelName": newModelname, "modelID": modelID})
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Model {modelID} has been updated to {newModelname}")
    return Response("Model updated", 200)

def deleteModel(modelID):
    if not isModelIDValid(modelID):
        return errorHandler("Model ID is not valid", "INPUT_EXCEPTION")
    if not modelIDExists(modelID):
        return errorHandler("Model ID does not exist", "INPUT_EXCEPTION")
    con, cur = connect()
    cur.execute("DELETE FROM model WHERE id = :modelID", {"modelID": modelID})
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Model {modelID} has been deleted")
    return Response("Model deleted", 200)


### Texture management ###

def textureIDExists(textureID):
    isTextureIDValid(textureID)
    con, cur = connect()
    res = cur.execute("SELECT id FROM texture WHERE id = :textureID", {"textureID": textureID})
    closeConnection(con)
    return len(res.fetchall()) > 0

def generateTextureID():
    id = uniqueID()
    while textureIDExists(id):
        id = uniqueID()
    return id


# Texture management functions #
def createTexture(modelID):
    if not isModelIDValid(modelID):
        return errorHandler("Model ID is not valid", "INPUT_EXCEPTION")
    if not modelIDExists(modelID):
        return errorHandler("Model ID does not exist", "INPUT_EXCEPTION")
    con, cur = connect()
    id = uniqueID()
    cur.execute("INSERT INTO texture VALUES (:textureID, :modelID)", {"textureID": id, "modelID": modelID})
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Texture {id} of model {modelID} has been created")
    return Response("Texture created", 200)    

def deleteTexture(textureID):
    if not isTextureIDValid(textureID):
        return errorHandler("Texture ID is not valid", "INPUT_EXCEPTION")
    if not textureIDExists(textureID):
        return errorHandler("Texture ID does not exist", "INPUT_EXCEPTION")
    con, cur = connect()
    cur.execute("DELETE FROM texture WHERE id = :textureID", {"textureID": textureID})
    con.commit()
    closeConnection(con)
    serverLogger.info(f"Texture {textureID} has been deleted")
    return Response("Texture deleted", 200)
"""
