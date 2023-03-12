from flask import Response
import logging
import uuid
import json

errorClasses = {
    "INPUT_EXCEPTION": {
        "name": "InputException",
        "code": 400
    },
    "NOT_AUTHORIZED": {
        "name": "NotAuthorized",
        "code": 401
    },
    "CONNECTION_EXCEPTION": {
        "name": "ConnectionException",
        "code": 500
    },
    "NOT_IMPLEMENTED": {
        "name": "NotImplemented",
        "code": 501
    }
}

# Create a logger to manage the errors of the user
logger = logging.getLogger("userLogger")
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler("logs/user.log")
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

# Create a logger to manage the errors of the server
serverLogger = logging.getLogger("applicationLogger")
serverLogger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler("logs/application.log")
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fileHandler.setFormatter(formatter)
serverLogger.addHandler(fileHandler)


def errorHandler(errorText, errorClass):
    if errorClass not in errorClasses:
        raise Exception("Invalid error class")
    
    errorUID = uuid.uuid4().hex

    if errorClasses[errorClass]["code"] >= 400 and errorClasses[errorClass]["code"] < 500:
        logger.error("Error ID: " + errorUID + " - " + errorText)
    else:
        serverLogger.error("Error ID: " + errorUID + " - " + errorText)

    return Response(json.dumps({
        "error": errorText,
        "errorType": errorClasses[errorClass]["name"],
        "logID": errorUID
    }), status=errorClasses[errorClass]["code"], mimetype='text/plain')


def errorID():
    return uuid.uuid4().hex

class ApplicationSpecificException(Exception):
    pass