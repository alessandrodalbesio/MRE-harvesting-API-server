# API Server
This repository has been developed as part of the project **"Mixed Reality Environment For Harvesting Study"** done by Alessandro Dalbesio.


## Getting started
This repository contains all the files needed to implement a server on a Raspberry Pi which can be used to manage all the files and texture needed in a virtual environment. <br><br>
After the installation as soon as you will turn on the Raspberry it will: 
- Act as an Access Point to create a private network
- Act as a DNS Server
- Act as an API Server
- Act as a Websocket Server
- Act as a proxy to serve all the static files required

All the devices should be connected to the WiFi of the Raspberry. <br>
To have access to internet you should connect the Raspberry with an ethernet connection (the WiFi is needed!). <br><br>
A schema of the server is displayed below: <br>
![Alt Text](readme/server-schema.png)

## Installation
Flash into a microSD (use at least 16 GB) the Raspberry Pi OS with Desktop 32/64 bit (Raspberry Pi Imager is suggested for this task) and setup the device.<br>
You should be able also to use other OS but you need to be sure that they are Debian based (or the installation script will not work).<br>
Don't use the WiFi to connect the device to the internet but use the Ethernet cable.
### Set up the Raspberry Hotspot
To create an hotspot with Raspberry Pi please follow [this tutorial](https://www.tomshardware.com/how-to/raspberry-pi-access-point).<br>
The name you will choose for the network and its password is not important for the installation even if it's highly recomended to use a strong password.<br>

### Installation
To install the server you should follow these steps:
1. Open a new terminal 
2. Create a new directory
```bash
sudo mkdir /home/<username>/server
```
The default username is <b>pi</b>. <br>
3. Clone the repository
```bash
git clone https://gitlab.epfl.ch/create-lab/sensing-with-vr/api-server.git /home/<username>/server
```
It will ask you to insert your credentials. You should use the username and the access token generated to access <code>gitlab.epfl.ch</code> (the access token will be needed also in the next sections).<br>
4. After cloning the repository move to the folder
```bash
cd /home/<username>/server
```
5. Create a file called <code>parameters.env</code> and write inside it the following parameters:
```bash
website_repo_url="create-lab/sensing-with-vr/user-interface"
websocket_server_repo_url="create-lab/sensing-with-vr/websocket-server"
api_server_repo_url="create-lab/sensing-with-vr/api-server"
api_port=9000
websocket_port=9001
domain_name="virtualenv.epfl.ch"
username="..."
access_token="..."
```
Above the default parameters are displayed. You should modify them to make the server compatible with your needs. A brief description of the parameters is provided below:
- <code>website_repo_url</code>: The repository of the user interface. If you want to use the default user interface you should write <code>create-lab/sensing-with-vr/user-interface</code>. If you want to use a custom user interface you should write the repository of the user interface you want to use.
- <code>websocket_server_repo_url</code>: The repository of the websocket server. If you want to use the default websocket server you should write <code>create-lab/sensing-with-vr/websocket-server</code>. If you want to use a custom websocket server you should write the repository of the websocket server you want to use.
- <code>api_server_repo_url</code>: The repository of the API server. You should not modify this parameter.
- <code>api_port</code>: The port used by the API server.
- <code>websocket_port</code>: The port used by the websocket server.
- <code>domain_name</code>: The domain name that you want to use
- <code>username</code>: The username of the account used to access <code>gitlab.epfl.ch</code> (it is your email without the @epfl.ch)
- <code>access_token</code>: The access token generated to access <code>gitlab.epfl.ch</code>

Take into account that all the <code>.env</code> files are ignored so that you don't push your credentials by mistake on the repository.<br>
At the end of the installation script the folder will be deleted so you don't need to worry about leaving your credentials on the Raspberry. If you wish after completing the installation you can delete the access token from your account. <br><br>
<b>IMPORTANT</b>: When you are creating the <code>parameters.env</code> file you MUST use as end of line character the <code>LF</code> character. If you use the <code>CRLF</code> character the installation will fail. <br>
If you are using Visual Studio Code you can change the end of line character by clicking on the bottom right corner of the editor and selecting <code>LF</code>.<br>

6. Run the installation scripts
```bash
sudo bash ./install.sh
```
This script will install all the needed components and it will take a while. <br>
If the installation has been succesful if you try to access the domain name you should see the user interface.<br>

## Code Structure
The code structure is:
```bash
├───index.py # It contains the Flask app definition
├───install.sh # Script that handles the installation
└───modules
    ├───db    
    │   ├─── connection.py # Handles the connection
    │   ├─── models.py # Handles the database management for the models
    │   └─── textures.py # Handles the database management for the textures
    ├───colors.py # Utilities functions for color management
    ├───logging.py # Management of the errors
    ├───serverImplementation.py # Implementation of all the functions
    └───settings.py # Main settings of the application

```

## User Interface
You should define the user interface repository url inside the <code>install.sh</code> at the following line of code:
```bash
website_repo_url=""
```
You can both choose to use the default user interface (its repository is [here](https://gitlab.epfl.ch/create-lab/sensing-with-vr/user-interface)) or create a new one. <br>
If you want to create a new user interface you should have a look at <code>index.py</code> for the endpoints available.


## WebSocket Server
You should define the websocket repository url inside the <code>install.sh</code> at the following line of code:
```bash
websocket_server_repo_url=""
```
You can both choose to use the default user interface (its repository is [here](https://gitlab.epfl.ch/create-lab/sensing-with-vr/websocket-server)) or create a new one. <br>
The Websocket Server choosen doesn't affect the API server but affect the ability of the User Interface and the Headset to communicate between each other.

## Errors management
All the errors produced by the server will be writen in files available in the folder <code>/var/www/API</code>. In this folder there will be both the file for the errors generated from the server and the file for the errors generated by <code>supervisord</code> which is a process control system used to manage the server <br>
If something goes wrong the server will generate automatically an unique ID (that will be shown on the user interface) that can be used to identify the error.

## Development conditions
The system has been developed in the following conditions:
- Python 3.11
- Raspberry Pi OS 32-bit / 64-bit with desktop kernel version 5.15 and Debian version 11
- Raspberry Pi 3 Model B+ (even if it should work also with the higher models)


## Authors
This repository is part of the project *"Mixed Reality Environment For Harvesting Study"* done by Alessandro Dalbesio.<br>
The project has been done in the CREATE LAB (EPFL).<br>
Professor: Josie Hughes<br>
Supervisor: Ilic Stefan<br>

## License
This project is under [MIT] license
