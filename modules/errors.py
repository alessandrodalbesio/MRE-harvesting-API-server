import logging, uuid, json, traceback
from functools import wraps


def errorID():
    return str(uuid.uuid4())

# Create a logger to manage the errors of the server
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler("logs.log")
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s at %(asctime)s \n%(message)s")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

def saveInfoLog(message):
    logger.info(message)

class InputException(Exception):
    def __init__(self, message, inputValue = ''):
        super().__init__(message)
        if inputValue != '':
            logger.warn("Error message: " + message + "\nInput value: " + inputValue.replace("\r", "").replace("\n", ""))
        else:
            logger.warn("Error message: " + message )
    def errorToJson(self):
        return json.dumps({'message': str(self)})

class SystemException(Exception):
    def __init__(self, message, tracebackError):
        super().__init__(message)
        errorID = manageSystemException(tracebackError)
        self.errorID = errorID
        
    def errorToJson(self):
        return json.dumps({'message': str(self), 'errorID': self.errorID})

def manageSystemException(tracebackError):
    generatedErrorID = errorID()
    logger.fatal("Tracking ID: " + generatedErrorID + "\n" + tracebackError)
    return generatedErrorID

def errorHandler():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except InputException as e:
                return e.errorToJson(), 400
            except SystemException as e:
                return e.errorToJson(), 500
            except Exception as e:
                errorTrackingID = manageSystemException(traceback.format_exc())
                return json.dumps({'error': 'An error occurred while retrieving the models list', 'errorTrackingID': errorTrackingID}), 500
        return wrapper
    return decorator