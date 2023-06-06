# Import all the needed global modules
from flask import Flask, request
import json

# Import all the needed local modules
from modules.logging import *
from modules.serverImplementation import *
from modules.settings import *

app = Flask(__name__)


##### MODELS MANAGEMENT #####

# Get a list of all models
@app.get('/models')
@errorHandler()
def getModelListHandler():
    return json.dumps(getModelsList()), 200

# Get information about a specific model based on the model id
@app.get('/model/modelID/<modelID>')
@errorHandler()
def getModelInfoByIDHandler(modelID):
    return json.dumps(getModelInfoByID(modelID)), 200

# Verify if a model name is already used
@app.get('/model/modelNameTaken/<modelName>')
@errorHandler()
def isModelNameTakenHandler(modelName):
    return json.dumps({'modelNameAlreadyUsed': modelNameAlreadyUsed(modelName)}), 200

# Get information about a specific model based on the model name
@app.get('/model/modelName/<modelName>')
@errorHandler()
def getModelInfoByNameHandler(modelName):
    return json.dumps(getModelInfoByName(modelName)), 200

# Data creation #

# Create a new model
@app.post('/model')
@errorHandler()
def index():
    if 'model' in request.files and 'modelName' in request.form and 'textureType' in request.form and 'cameraInfo' in request.form and 'modelWithTexturePreview' in request.files:
        cameraInfo = json.loads(request.form['cameraInfo'])
        # Test the camera informations
        if not arePreviewInfoValid(cameraInfo):
            raise InputException('Invalid camera info')

        # Manage the loading of the model and of its texture
        modelID = createModel(request.form['modelName'], request.files['model'], cameraInfo)

        # Select the texture type and verify that the required parameters are present
        if request.form['textureType'] == 'color' and 'textureColor' in request.form:
            createTextureByColor(modelID, request.form['textureColor'], request.files['modelWithTexturePreview'], True)
        elif request.form['textureType'] == 'image' and 'textureImage' in request.files:
            createTextureByImage(modelID, request.files['textureImage'], request.files['modelWithTexturePreview'], True)
        else:
            deleteModel(modelID)
            raise InputException('No texture type specified or the specified one is not valid')
        return 'Model created successfully', 200
    else:
        # Manage the input exception based on the missing parameters
        if 'model' not in request.files:
            raise InputException('No model file')
        if 'modelName' not in request.form:
            raise InputException('No model name')
        if 'textureType' not in request.form:
            raise InputException('No texture input type')
        if 'cameraInfo' not in request.form:
            raise InputException('No camera info')
        if 'modelWithTexturePreview' not in request.files:
            raise InputException('No camera photo')

# Data update #

# Update the name of the model with the modelID
@app.put('/model/<modelID>')
@errorHandler()
def handleModelUpdate(modelID):
    if 'modelName' in request.form:
        updateModelName(modelID, request.form['modelName'])
        return 'Model updated successfully', 200
    else:
        raise InputException('No model name')

# Data cancellation #

# Delete the model with the modelID
@app.delete('/model/<modelID>')
@errorHandler()
def handleModelDelete(modelID):
    deleteModel(modelID)
    return 'Model deleted successfully', 200



##### TEXTURES MANAGEMENT #####

# Delete a texture with a specific textureID
@app.delete('/texture/<textureID>')
@errorHandler()
def handleTextureDelete(textureID):
    deleteTexture(textureID)
    return 'Texture deleted successfully', 200

# Create a texture from a color definition
@app.post('/texture/color')
@errorHandler()
def handleColorTexture():
    if 'modelID' in request.form and 'textureColor' in request.form and 'modelWithTexturePreview' in request.files:
        textureInfo = createTextureByColor(request.form['modelID'], request.form['textureColor'], request.files['modelWithTexturePreview'], False)
        return json.dumps(textureInfo), 200
    else:
        if 'modelID' not in request.form:
            raise InputException('No model ID')
        if 'textureColor' not in request.form:
            raise InputException('No texture color')
        if 'modelWithTexturePreview' not in request.files:
            raise InputException('No texture preview')

# Create a texture from an image
@app.post('/texture/image')
@errorHandler()
def handleImageTexture():
    if 'modelID' in request.form and 'textureImage' in request.files and 'modelWithTexturePreview' in request.files:
        textureInfo = createTextureByImage(request.form['modelID'], request.files['textureImage'], request.files['modelWithTexturePreview'], False)
        return json.dumps(textureInfo), 200
    else:
        if 'modelID' not in request.form:
            raise InputException('No model ID')
        if 'textureImage' not in request.files:
            raise InputException('No texture image')
        if 'modelWithTexturePreview' not in request.files:
            raise InputException('No texture preview')

# Set the default texture of a model
@app.put('/texture/default/<modelID>')
@errorHandler()
def handleDefaultTexture(modelID):
    if 'textureID' in request.form:
        setDefaultTexture(modelID, request.form['textureID'])
        return 'Default texture set successfully', 200
    else:
        raise InputException('No texture ID')


##### SETTINGS MANAGEMENT #####
# Get the list of all the settings of the server (needed from the clients to have consistency when they are updated)
@app.get('/settings')
@errorHandler()
def settingsHandler():
    return json.dumps(SETTINGS_ALL), 200

# Run the app when the program starts!
if __name__ == '__main__':
    app.run(host = HOST, port = PORT, debug = DEBUG)
