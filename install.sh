#!/bin/sh

WEBSITE_REPO_URI="" # This is the uri of the website repo

# YOU SHOULD NOT EDIT THE LINE BELOW IF YOU HAVE FOLLOWED THE INSTALLATION INSTRUCTIONS #

# General parameter settings
HOST="127.0.0.1"
SERVER_PORT=9000
DOMAIN="virtualenv.epfl.ch"

# Nginx endpoints
API_ENDPOINT="/api"
MODELS_FOLDER_ENDPOINT="/models"

# Folder settings
SERVER_FOLDER= "/var/www/API"
UI_FOLDER="/var/www/html"
MODELS_FOLDER="/var/www/models"
ERROR_PAGES_FOLDER="/var/www/html/error-pages"

# Verify that all the needed components has been installed correctly

    # Verify that WEBSITE_REPO_URI is not empty
    if [ -z "${WEBSITE_REPO_URI}" ]; then
        echo "WEBSITE_REPO_URI is empty. Please fill it before running this script."
        exit 1
    fi

    # Verify that the system is a raspberry pi
    if [ ! "$(uname -m)" = "armv7l" ]; then
        echo "This script is only for Raspberry Pi. If you want to install it to other systems you should before modify the install.sh."
        exit 1
    fi

    # Verify that the file is insider the SERVER_FOLDER folder otherwise exit
    if [ ! "$(pwd)" = "${SERVER_FOLDER}" ]; then
        echo "This script should be run inside the ${SERVER_FOLDER} folder."
        exit 1
    fi

    # Verify that Nginx is installed
    if [ ! -x "$(command -v nginx)" ]; then
        echo "Nginx is not installed. Please install it before running this script."
        exit 1
    fi

    # Verify that the folder /var/www/ exists
    if [ ! -d "/var/www/" ]; then
        echo "The folder /var/www/ does not exist. If you have modified the Nginx installation folders you should modify also the install.sh file."
        exit 1
    fi

    # Verify that ufw is installed
    if [ ! -x "$(command -v ufw)" ]; then
        echo "UFW is not installed. Please install it before running this script."
        exit 1
    fi

    # Verify that SSH is allowed in ufw otherwise allow it
    if [ ! "$(sudo ufw status | grep 'OpenSSH')" ]; then
        sudo ufw allow OpenSSH
    fi

    # Verify that Nginx HTTP is allowed in ufw otherwise allow it
    if [ ! "$(sudo ufw status | grep 'Nginx HTTP')" ]; then
        sudo ufw allow 'Nginx HTTP'
    fi

    # Verify that ufw is enabled otherwise enable it
    if [ ! "$(sudo ufw status | grep 'Status: active')" ]; then
        sudo ufw enable
    fi

    # Verify that python is installed and if you should use python or python3
    if [ -x "$(command -v python3)" ]; then
        PYTHON="python3"
    elif [ -x "$(command -v python)" ]; then
        PYTHON="python"
    else
        # Install python
        sudo apt-get install python3
        PYTHON="python3"
    fi


# Install all the needed softwares

    # Update and upgrade the system
    sudo apt-get update
    sudo apt-get upgrade -y

    # Install supervisor (Needed to run the server as a service)
    sudo apt-get install supervisor -y

    # Install dnsmasq (This is used as a DNS server)
    sudo apt-get install dnsmasq -y


# Set the configuration files in Nginx

    # Nginx configuration file
    NGINX_CONF_FILE="user www-data;
    worker_processes auto;
    pid /run/nginx.pid;
    include /etc/nginx/modules-enabled/*.conf;

    events {
        worker_connections 768;
        # multi_accept on;
    }

    http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        types_hash_max_size 2048;
        # server_tokens off;

        server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;

        # gzip_vary on;
        # gzip_proxied any;
        # gzip_comp_level 6;
        # gzip_buffers 16 8k;
        # gzip_http_version 1.1;
        # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
        client_max_body_size 100M;
    }


    #mail {
    #	# See sample authentication script at:
    #	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
    #
    #	# auth_http localhost/auth.php;
    #	# pop3_capabilities "TOP" "USER";
    #	# imap_capabilities "IMAP4rev1" "UIDPLUS";
    #
    #	server {
    #		listen     localhost:110;
    #		protocol   pop3;
    #		proxy      on;
    #	}
    #
    #	server {
    #		listen     localhost:143;
    #		protocol   imap;
    #		proxy      on;
    #	}
    #}
    "   

    # Delete the content in nginx.conf and add the content in NGINX_CONF_FILE
    echo "${NGINX_CONF_FILE}" | sudo tee /etc/nginx/nginx.conf > /dev/null

    # Nginx website file
    NGINX_WEBSITE_FILE="
    server {
        listen 80;
        server_name ${DOMAIN};

        location / {
            root ${UI_FOLDER};
            index index.html;
        }

        location ${API_ENDPOINT} {
            proxy_pass http://${HOST}:${SERVER_PORT}/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }

        location ${MODELS_FOLDER_ENDPOINT} {
            alias ${MODELS_FOLDER};
            autoindex on;
        }

        error_page 404 /404.html;
        location = /404.html {
            root ${ERROR_PAGES_FOLDER};
            internal;
        }
    }"

    sudo echo "${NGINX_CONFIGURATION_FILE}" > /etc/nginx/sites-available/raspberryvr # Set the nginx configuration file
    sudo ln -s /etc/nginx/sites-available/raspberryvr /etc/nginx/sites-enabled/raspberryvr  
    
    # Delete the default nginx website
    sudo rm -rf /etc/nginx/sites-enabled/default
    sudo rm -rf /etc/nginx/sites-available/default

# Create all the needed folders and delete the default ones
    # Delete the default nginx folder
    sudo rm -rf /var/www/html

    #  Create all the folders
    sudo mkdir -p ${UI_FOLDER} # Create the UI folder
    sudo mkdir -p ${MODELS_FOLDER} # Create the models folder    

    # Clone the UI repo
    git clone ${UI_REPO_URI} ${UI_FOLDER_NAME}


# Create the virtual environments and set up everything
    # Move to the server repo folder
    cd ${SERVER_FOLDER}

    # Create the server virtual environment
    sudo ${PYTHON} -m venv ${SERVER_FOLDER}/.venv
    sudo ${SERVER_FOLDER}/.venv/bin/pip install -r ${SERVER_FOLDER}/requirements.txt

    # Clone the server repo #
    git clone ${SERVER_REPO_URI} ${SERVER_FOLDER_NAME}

    # Create the configuration file for the server for supervisor and run it with gunicorn
    SERVER_CONF_FILE="[program:raspberryvr]
    directory=${SERVER_FOLDER}
    command=${SERVER_FOLDER}.venv/bin/gunicorn index:app -b localhost:9000
    autostart=true
    autorestart=true
    stderr_logfile=${SERVER_FOLDER}/raspberryvr_supervisorctl.err.log
    stdout_logfile=${SERVER_FOLDER}/raspberryvr_supervisorctl.out.log
    user=pi
    "
    sudo echo "${SERVER_CONF_FILE}" > /etc/supervisor/conf.d/raspberryvr.conf
    sudo supervisorctl reread
    sudo supervisorctl update

# Create the new DNS with dnsmasq
    # Create the new DNS file
    DNS_FILE="address=/${DOMAIN}/${HOST}"
    sudo echo "${DNS_FILE}" > /etc/dnsmasq.d/raspberryvr.conf

    # Restart the dnsmasq service
    sudo systemctl restart dnsmasq

# Set the timezone to Europe/Zurich
    sudo timedatectl set-timezone Europe/Zurich

# Delete the install.sh file when done and restart the system
sudo rm -- "$0"
sudo reboot