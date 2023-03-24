# Import all the needed global modules
from flask import Flask, request
from flask_cors import CORS
import traceback
import json

# Import all the needed local modules
from modules.errors import *
from modules.serverImplementation import *
from modules.settings import *

app = Flask(__name__)
CORS(app)


@app.get('/models')
@errorHandler()
def modelsList():
    return json.dumps(getModelsList()), 200

@app.post('/model')
@errorHandler()
def index():
    if 'model' in request.files and 'modelName' in request.form and 'textureType' in request.form:
        # Test the camera informations
        if 'cameraInfo' in request.form:
            if arePreviewInfoValid(request.form['cameraInfo']):
                if not 'cameraPhoto' in request.files:
                    raise InputException('No camera photo')
                else:
                    cameraInfo = json.loads(request.form['cameraInfo'])
            else:
                raise InputException('Invalid camera info', request.form['cameraInfo'])
        else:
            raise InputException('No camera info')

        # Manage the loading of the model and of its texture
        modelID = createModel(request.form['modelName'], request.files['model'], cameraInfo)

        # Select the texture type and verify that the required parameters are present
        if request.form['textureType'] == 'color' and 'textureColor' in request.form:
            createTextureByColor(modelID, request.form['textureColor'], request.files['cameraPhoto'], True)
        elif request.form['textureType'] == 'image' and 'textureImage' in request.files:
            createTextureByImage(modelID, request.files['textureImage'], request.files['cameraPhoto'], True)
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

@app.get('/model/<modelID>')
@errorHandler()
def model(modelID):
    return json.dump(getModelInfoByID(modelID)), 200


@app.post('/model/<modelID>')
@errorHandler()
def updateModel(modelID):
    if 'modelName' in request.form:
        updateModelName(modelID, request.form['modelName'])
        return 'Model updated successfully', 200
    else:
        raise InputException('No model name')


@app.delete('/model/<modelID>')
@errorHandler()
def handleModelDelete(modelID):
    deleteModel(modelID)
    return 'Model deleted successfully', 200


####################


# Run the app when the program starts!
if __name__ == '__main__':
    app.run(debug=DEBUG_ACTIVE, use_reloader=USE_RELOADER, host=HOST, port=PORT)
