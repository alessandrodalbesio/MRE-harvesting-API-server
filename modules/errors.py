import logging, uuid, os

# If the directory logs doesn't exist, create it
if not os.path.exists("logs"):
    os.makedirs("logs")

# Create a logger to manage the errors of the user
logger = logging.getLogger("userLogger")
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler("logs/user.log")
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s \n%(message)s")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

# Create a logger to manage the errors of the server
serverLogger = logging.getLogger("applicationLogger")
serverLogger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler("logs/application.log")
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s \n%(message)s")
fileHandler.setFormatter(formatter)
serverLogger.addHandler(fileHandler)

def errorID():
    return str(uuid.uuid4())

class InputException(Exception):
    def __init__(self, message, inputValue = ''):
        super().__init__(message)
        inputValue = inputValue.replace("\r", "").replace("\n", "")
        logger.error("Error message: "+message+"\nInput value: "+inputValue+"\n")

def manageSystemException(message, tracebackError):
    generatedErrorID = errorID()
    serverLogger.error("Tracking ID: "+generatedErrorID+"\n"+tracebackError+"\n")
    return message+" Tracking ID: "+generatedErrorID

class SystemException(Exception):
    def __init__(self, message, tracebackError):
        super().__init__(manageSystemException(message, tracebackError))