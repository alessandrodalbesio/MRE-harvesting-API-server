# This file will reset everything in the database, in the logs and in the module folder
# Please use this file with caution

import modules.settings as settings
import os
import shutil

# Reset the database
def resetDatabase():
    # Delete the database file
    try:
        if os.path.exists(settings.DB_NAME):
            print("Deleting database...")
            os.remove(settings.DB_NAME)
            return True
        return False
    except:
        print("Error while deleting the database file")

# Reset the logs
def resetLogs():
    # Delete the logs folder
    try:
        if os.path.exists('logs.log'):
            print("Deleting logs...")
            os.remove('logs.log')
            return True
        return False
    except:
        print("Error while deleting the logs folder")

# Reset the models folder
def deleteModelFolder():
    # Delete the models folder
    try:
        if os.path.exists(settings.MODELS_FOLDER):
            print("Deleting models folder...")
            shutil.rmtree(settings.MODELS_FOLDER)
            return True
        return False
    except:
        print("Error while deleting the models folder")

if __name__ == "__main__":
    if input("Are you sure you want to reset everything? (y/n): ") != 'y':
        exit()
    if resetDatabase() or resetLogs() or deleteModelFolder():
        print("Reset completed")
    else:
        print("Nothing to reset")