#!/bin/bash
# This file has been created specifically for Debian Distributions
# Some changes may be needed for other distributions

# To define the parameters copy the following in a file called "parameters.env" and change the values
# Then run this script with the command "sudo bash install.sh"
##### COPY BELOW THIS LINE #####
# Insert the gitlab repository urls (after the https://gitlab.epfl.ch/ part)
# website_repo_url="create-lab/sensing-with-vr/user-interface"
# websocket_server_repo_url="create-lab/sensing-with-vr/websocket-server"
# api_server_repo_url="create-lab/sensing-with-vr/api-server"
# api_port=9000
# websocket_port=9001
# domain_name="virtualenv.epfl.ch"
# Insert your git credentials for gitlab.epfl.ch
# username="" # Without the @epfl.ch
# access_token=""
##### COPY ABOVE THIS LINE #####

# Step 0: Definition of the parameters and initial checking
    # Load the parameters from parameters.env
    if [ -f parameters.env ]; then
        source parameters.env
    fi

    # Check if the parameters have been defined
    if [ -z "$website_repo_url" ] || [ -z "$websocket_server_repo_url" ] || [ -z "$api_server_repo_url" ] || [ -z "$api_port" ] || [ -z "$websocket_port" ] || [ -z "$domain_name" ] || [ -z "$username" ] || [ -z "$access_token" ]; then
        echo "Please define the parameters in the file parameters.sh"
        exit 1
    fi

    # Add the gitlab credentials to the urls
    website_repo_url="https://$username:$access_token@gitlab.epfl.ch/$website_repo_url"
    websocket_server_repo_url="https://$username:$access_token@gitlab.epfl.ch/$websocket_server_repo_url"
    api_server_repo_url="https://$username:$access_token@gitlab.epfl.ch/$api_server_repo_url"

    # Verify that the system is Debian
    if [ ! -f /etc/debian_version ]; then
        echo "This script is only for Debian distributions"
        exit 1
    fi

    # Verify that the system has git installed and install it if not
    if [ ! -f /usr/bin/git ]; then
        sudo apt-get install git -y
    fi

    # Get the current device ip on wlan0
    ip=$(ip addr show wlan0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)

    # Apply to the ip the mask 24
    router_ip=$(echo $ip | cut -d. -f1-3).0

# Step 1: Set the static IP
    dhcpcd_conf_file="
    # Inform the DHCP server of our hostname for DDNS.
    hostname

    # Use the hardware address of the interface for the Client ID.
    clientid

    # Persist interface configuration when dhcpcd exits.
    persistent

    # Rapid commit support.
    # Safe to enable by default because it requires the equivalent option set
    # on the server to actually work.
    option rapid_commit

    # A list of options to request from the DHCP server.
    option domain_name_servers, domain_name, domain_search, host_name
    option classless_static_routes
    # Respect the network MTU. This is applied to DHCP routes.
    option interface_mtu

    # A ServerID is required by RFC2131.
    require dhcp_server_identifier

    # Generate Stable Private IPv6 Addresses based from the DUID
    slaac private

    # Static IP configuration for WLAN
    interface wlan0
    static ip_address=$ip/24
    static routers=$router_ip
    static domain_name_server=$router_ip"

    sudo rm /etc/dhcpcd.conf
    sudo touch /etc/dhcpcd.conf
    # Save the file into the other file without outputting it
    echo "$dhcpcd_conf_file" | sudo tee /etc/dhcpcd.conf > /dev/null

# Step 2: Update and upgrade
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt autoremove -y

# Step 3: Install Nginx
    sudo apt-get install nginx -y

# Step 4: Configure Nginx
    nginx_conf_file='
    user www-data;
    worker_processes auto;
    pid /run/nginx.pid;
    include /etc/nginx/modules-enabled/*.conf;

    events {
        worker_connections 2000;
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
    }'
    nginx_proxy_file='
    server {
        listen 80;
        server_name '$domain_name';
        error_log /var/www/server.error.log;
        
        location / {
            root /var/www/website;
            index index.html;
        }

        location /ws {
            proxy_pass http://127.0.0.1:'$websocket_port'/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
        }

        location /api {
            proxy_pass http://127.0.0.1:'$api_port'/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass_request_headers on;
        }

        location /models {
            alias /var/www/models/;
            autoindex off;
        }
    }'

    # Copy the nginx configuration file
    sudo rm /etc/nginx/nginx.conf
    sudo touch /etc/nginx/nginx.conf
    # Copu the file while keeping the new lines
    
    echo "$nginx_conf_file" | sudo tee -a /etc/nginx/nginx.conf > /dev/null

    # Copy the nginx proxy file
    sudo rm /etc/nginx/sites-available/*
    sudo rm /etc/nginx/sites-enabled/*
    sudo touch /etc/nginx/sites-available/virtual_env
    echo "$nginx_proxy_file" | sudo tee -a /etc/nginx/sites-available/virtual_env > /dev/null
    sudo ln -s /etc/nginx/sites-available/virtual_env /etc/nginx/sites-enabled/virtual_env

# Step 5: Create the directories and clone the repositories
    # Remove all the material that is in the folder /var/www
    sudo rm -rf /var/www/*

    # Manage website
    sudo mkdir -p /var/www/website
    sudo git clone $website_repo_url /var/www/website
    website_settings='{
    "SELF_DOMAIN": "http://'$domain_name'/",
    "API_DOMAIN": "http://'$domain_name'/api",
    "MODELS_FOLDER": "http://'$domain_name'/models/",
    "WEBSOCKET_DOMAIN": "ws://'$domain_name'/ws"
    }'
    echo $website_settings | sudo tee -a /var/www/website/settings.json > /dev/null

    # Manage websocket server
    sudo mkdir -p /var/www/websocket
    sudo git clone ${websocket_server_repo_url} /var/www/websocket
    sudo python -m venv /var/www/websocket/.venv
    sudo /var/www/websocket/.venv/bin/pip install -r /var/www/websocket/requirements.txt
    websocket_server_settings='{
        "WEBSOCKET_SERVER_ADDRESS": "127.0.0.1",
        "WEBSOCKET_SERVER_PORT": '$websocket_port'
    }'
    echo $websocket_server_settings | sudo tee -a /var/www/websocket/modules/settings.json > /dev/null

    # Manage API server
    sudo mkdir -p /var/www/API
    sudo git clone $api_server_repo_url /var/www/API
    sudo python -m venv /var/www/API/.venv
    sudo /var/www/API/.venv/bin/pip install -r /var/www/API/requirements.txt

# Step 6: Install supervisor
    sudo apt-get install supervisor -y

# Step 7: Configure supervisor
    supervisor_api_file="
    [program:api]
    directory=/var/www/API
    command=/var/www/API/.venv/bin/gunicorn index:app -b localhost:$api_port
    autostart=true
    autorestart=true
    stderr_logfile=/var/www/API/supervisor.err.log
    stdout_logfile=/var/www/API/supervisor.out.log"

    supervisor_websocket_file="
    [program:websocket]
    command=/var/www/websocket/.venv/bin/python /var/www/websocket/index.py
    autostart=true
    autorestart=true
    stderr_logfile=/var/www/websocket/supervisor.err.log
    stdout_logfile=/var/www/websocket/supervisor.out.log"

    # Remove all the files in the folder /etc/supervisor/conf.d
    sudo rm -rf /etc/supervisor/conf.d/*
    # Create the first file called api.conf
    sudo touch /etc/supervisor/conf.d/api.conf
    echo "$supervisor_api_file" | sudo tee -a /etc/supervisor/conf.d/api.conf > /dev/null
    # Create the second file called websocket.conf
    sudo touch /etc/supervisor/conf.d/websocket.conf
    echo "$supervisor_websocket_file" | sudo tee -a /etc/supervisor/conf.d/websocket.conf > /dev/null
    sudo supervisorctl reread
    sudo supervisorctl update

# Step 8: Install dnsmasq
    sudo apt-get install dnsmasq -y

# Step 9: Configure dnsmasq
    # Stop and disable systemd-resolved
    sudo systemctl disable systemd-resolved
    sudo systemctl stop systemd-resolved

    # Define dnsmasq configuration file
    dnsmasq_conf_file="
    # Configuration file for dnsmasq.

    # Never forward plain names (without a dot or domain part)
    domain-needed

    # Never forward addresses in the non-routed address spaces.
    bogus-priv

    # Define the virtualenv address
    address=/$domain_name/$ip
    
    # Set the DNS servers
    server=8.8.8.8
    server=8.8.4.4"

    # Delete the file /etc/dnsmasq.conf
    sudo rm /etc/dnsmasq.conf
    sudo touch /etc/dnsmasq.conf
    echo "$dnsmasq_conf_file" | sudo tee -a /etc/dnsmasq.conf > /dev/null

# Step 10: Final configurations
    #sudo rm $(pwd)/parameters.env
    #sudo rm $(pwd)/install.sh
    sudo reboot