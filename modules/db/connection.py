import sqlite3, uuid, traceback
from modules.errors import *
from modules.settings import *

### Global functions definition ###
def connect():
    try:
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
            'isDefault' BOOLEAN DEFAULT 0,
            'isColor' BOOLEAN DEFAULT 0,
            'colorHex' CHAR(7) DEFAULT NULL,
            'isImage' BOOLEAN DEFAULT 0,
            'extension' VARCHAR(4) DEFAULT NULL
        )""")
        return con, cur
    except sqlite3.Error as err:
        raise SystemException("Something went wrong during the creation of the connection to the database", traceback.format_exc())
    except Exception as err:
        raise SystemException("Something went wrong", traceback.format_exc())

def closeConnection(con):
    try:
        con.close()
    except sqlite3.Error as err:
        raise SystemException("Something went wrong during the closing of the connection to the database", traceback.format_exc())

def uniqueID():
    try:
        generatedID = str(uuid.uuid4().hex)
        return generatedID
    except Exception as err:
        raise SystemException("Something went wrong while generating a unique ID", traceback.format_exc())

