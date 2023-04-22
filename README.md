# VR Server
## Introduction 

## Requirements

## Installation
To install the server you just have to follow this operations:
```bash
# Clone the Gitlab repo

# Move to the place where the Gitlab repo has been saved

# Execute the installation file
./install.sh
```
The <b>install.sh</b> file will perform the following operations:
- Make the raspberry behave as an access point
- Copy all the files inside the folder <b>./server</b> (relative to the rootystem)
- Create the virtual environment and install all the needed modules reported in reqirements.txt
- Delete all the files that are not needed for production present in the github repo
- Activate the server and set it up to run at the server startup
- Restart the device

## Structure
In the following it's displayed the structure of this directory with the list of all the directories and files.
```bash
├───index.py    # It contains the Flask app definition
├───modules
|   ├───db.py    # Contains all the needed function to communicate with the db
|   ├───errors.py   # Management of the errors
|   ├───serverImplementation.py    # Implementation of all the functions
|   └───settings.py    # Main settings of the application
└───website
    ├───index.html    # Main file with the management of the active model and of the textures
    ├───new-model.html    # Management of new models upload
    └───src
        ├───css
        ├───img
        └───js
```

## Credits
This project has been done by Alessandro Dalbesio as part of a semester project done at [CREATE Lab](https://www.epfl.ch/labs/create/).

## License
[ISC]
