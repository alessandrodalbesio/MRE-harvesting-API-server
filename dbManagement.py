import sqlite3
import uuid
from errorHandling import *
from settings import *


### Global functions definition ###
def connect():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS model (id CHAR({MODEL_ID_LENTGH}) PRIMARY KEY, name VARCHAR({MODEL_NAME_MAX_LENTGH}) NOT NULL)")
    cur.execute(f"CREATE TABLE IF NOT EXISTS texture (id CHAR({TEXTURE_ID_LENGTH}) PRIMARY KEY, idModel CHAR({MODEL_ID_LENTGH}), FOREIGN KEY (idModel) REFERENCES model(id))")
    cur.execute(f"CREATE TABLE IF NOT EXISTS lockOnModels (requesterID VARCHAR({REQUESTER_ID_MAX_LENGTH}) PRIMARY KEY, idModel CHAR({MODEL_ID_LENTGH}), FOREIGN KEY (idModel) REFERENCES model(id))")
    return con, cur

def closeConnection(con):
    con.close()

def uniqueID():
    return str(uuid.uuid4().hex)

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

# Input verification functions #
def isModelIDValid(modelID):
    return isinstance(modelID, str) and len(modelID) == MODEL_ID_LENTGH

def modelIDExists(modelID):
    isModelIDValid(modelID)
    con, cur = connect()
    res = cur.execute("SELECT id FROM model WHERE id = :modelID", {"modelID": modelID})
    closeConnection(con)
    return len(res.fetchall()) > 0

def isModelNameValid(modelName):
    return isinstance(modelName, str) and 0 < len(modelName) <= MODEL_NAME_MAX_LENTGH

def generateModelID():
    id = uniqueID()
    while modelIDExists(id):
        id = uniqueID()
    return id

def modelNameExists(modelName):
    isModelNameValid(modelName)
    con, cur = connect()
    res = cur.execute("SELECT id FROM model WHERE name = :modelName", {"modelName": modelName})
    closeConnection(con)
    return len(res.fetchall()) > 0


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

# Input verification functions #
def isTextureIDValid(textureID):
    return isinstance(textureID, str) and len(textureID) == TEXTURE_ID_LENGTH

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