from flask import Flask, request
from flask_socketio import SocketIO, ConnectionRefusedError, join_room, emit
from settings import *
import dbManagement as db
from serverFunctions import *


# GENERAL SETTINGS
app = Flask(__name__, static_url_path=STATIC_URL_PATH, static_folder=STATIC_FOLDER)
socketio = SocketIO(app)


# API GATEWAY DEFINITION

@app.route("/data", methods=["GET", "POST"])
def data():
    requesterID = request.headers.get('X-DEVICE-ID')
    if requesterID is None:
        return errorHandler("No device ID specified", "INPUT_EXCEPTION")
    
    if request.method == "GET":
        if requesterID == deviceID['CLIENT']:
            return getData()
        elif requesterID == deviceID['VR-HEADSET']:
            return retrieveVRData()
        else:
            return errorHandler("Your userID doesn't have any service associated with this method/endpoint", "NOT_IMPLEMENTED")
    elif request.method == "POST":
        if requesterID == deviceID['CLIENT']:
            if 'modelName' in request.form and 'modelOBJ' in request.files and 'modelIMG' in request.files:
                return createModel(request.form['modelName'], request.files['modelOBJ'], request.files['modelIMG'])
            else:
                return errorHandler("Invalid request", "INPUT_EXCEPTION")
        else:
            return errorHandler("Your userID doesn't have any service associated with this method/endpoint", "NOT_IMPLEMENTED")
    else:
        return errorHandler("Invalid request method", "NOT_IMPLEMENTED")

@app.route('/texture', methods=['POST', 'DELETE'])
def texture():
    requesterID = request.headers.get('X-DEVICE-ID')
    if requesterID is None:
        return errorHandler("No device ID specified", "INPUT_EXCEPTION")

    if requesterID == deviceID['CLIENT']:
        if request.method == 'POST':
            if 'textureIMG' in request.files:
                return createTexture(request.files['textureIMG'])
            else:
                return errorHandler("Invalid request", "INPUT_EXCEPTION")
        elif request.method == 'DELETE':
            if 'modelID' in request.form and 'textureID' in request.form:
                return deleteTexture(request.form['modelID'], request.form['textureID'])
            else:
                return errorHandler("Invalid request", "INPUT_EXCEPTION")
        else:
            return errorHandler("Invalid request method", "NOT_IMPLEMENTED")
    else:
        return errorHandler("Your userID doesn't have any service associated with this method/endpoint", "NOT_IMPLEMENTED")

        
"""
# WEBSOCKETS DEFINITION

@socketio.on('connect')
def manage_connection():
    if 'deviceID' not in request.args:
        if request.args['deviceID'] in deviceID:
            if request.args['deviceID'] == deviceID['CLIENT']:
                join_room('clientROOM')
            elif request.args['deviceID'] == deviceID['SYSTEM']:
                join_room('systemROOM')
            else:
                join_room('headsetROOM')
        else:
            raise ConnectionRefusedError('Non valid device ID')
    else:
        raise ConnectionRefusedError('No device ID specified')

@socketio.on('disconnect')
def manage_disconnection():
    db.unlockModel(request.sid)

@socketio.on('selectModelTexture')
def handle_model_texture_selection(modelID, textureID):
    emit('selectModelTexture', {'modelID': modelID, 'textureID': textureID}, to='clientROOM', include_self = False)
    emit('selectModelTexture', {'modelID': modelID, 'textureID': textureID}, to='headsetROOM', include_self = False)

@socketio.on('lockModel')
def lock_model(modelID):
    db.lockModel(modelID, request.sid)
    emit('lockModel', {'modelID': modelID}, to='clientROOM', include_self = False)

@socketio.on('unlockModel')
def unlock_model():
    modelID = db.unlockModel(request.sid)
    emit('unlockModel', {'modelID': modelID}, to='clientROOM')
"""

# INITIALIZE APP

if __name__ == "__main__":
    #db.unlockAllModels()
    socketio.run(app, host = HOST, port = PORT, debug = DEBUG_ACTIVE)