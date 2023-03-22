from flask import Flask, request
from flask_cors import CORS
import traceback
import json

from modules.serverImplementation import *

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path=STATIC_URL_PATH)
CORS(app)

# Create a route at the base URL
@app.post('/upload-model')
def index():
    try:
        if 'model' in request.files and 'modelName' in request.form and 'textureType' in request.form:
            # Test the camera informations
            if 'cameraInfo' in request.form:
                if areCameraInfoValid(request.form['cameraInfo']):
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
                createTextureByColor(modelID, request.form['textureColor'], request.files['cameraPhoto'])
                return 'Model created successfully', 200
            elif request.form['textureType'] == 'image' and 'textureImage' in request.files:
                createTextureByImage(modelID, request.files['textureImage'], request.files['cameraPhoto'])
                return 'Model created successfully', 200
            else:
                db.deleteModel(modelID)
                raise InputException('No texture type specified or the specified one is not valid')
        else:
            # Manage the input exception based on the missing parameters
            if 'model' not in request.files:
                raise InputException('No model file')
            if 'modelName' not in request.form:
                raise InputException('No model name')
            if 'textureType' not in request.form:
                raise InputException('No texture input type')
    except InputException as e:
        return str(e), 400
    except SystemException as e:
        return str(e), 500
    except Exception as e:
        return str(manageSystemException(str(e), traceback.format_exc())), 500

@app.get('/get-models')
def getModels():
    return 'Models', 200

# Run the app when the program starts!
if __name__ == '__main__':
    app.run(debug=DEBUG_ACTIVE, use_reloader=USE_RELOADER, host=HOST, port=PORT)
