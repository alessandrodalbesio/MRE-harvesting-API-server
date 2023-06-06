# !/bin/bash

# This file has been created specifically for Debian Distributions
# Some changes may be needed for other distributions

## CHANGE BELOW THIS LINE ##
#---------------------------#

website_repo_url=""
websocket_server_repo_url=""
api_server_repo_url=""

#-----------------------------------------#
## CHANGE ABOVE THIS LINE ##

# Step 0: Definition of the parameters and initial checking
    # Get script location
    script_path=$(dirname $(readlink -f $0))

    # Get nginx files location
    nginx_conf_file="$script_path/setup-files/nginx/nginx.conf"
    nginx_proxy_file="$script_path/setup-files/nginx/virtual_env"

    # Get supervisor files location
    supervisor_api_file="$script_path/setup-files/supervisor/api.conf"
    supervisor_websocket_file="$script_path/setup-files/supervisor/websocket.conf"

    # Get dnsmaq files location
    dnsmasq_conf_file="$script_path/setup-files/dnsmasq/dnsmasq.conf"

    # Get the dhcpd.conf file location
    dhcpd_conf_file="$script_path/setup-files/dhcpd/dhcpd.conf"

    # Verify that the system is Debian
    if [ ! -f /etc/debian_version ]; then
        echo "This script is only for Debian distributions"
        exit 1
    fi

    # Manage python
    if [ -f /usr/bin/python ]; then
        python=$(which python)
    elif [ -f /usr/bin/python3 ]; then
        python=$(which python3)
    else
        sudo apt-get install python3 -y
        python=$(which python3)
    fi

# Step 1: Set the static IP
    sudo cp $dhcpd_conf_file /etc/dhcpd.conf

# Step 2: Update and upgrade
    sudo apt-get update
    sudo apt-get upgrade -y

# Step 3: Install Nginx
    sudo apt-get install nginx -y

# Step 4: Configure Nginx
    sudo cp $nginx_conf_file /etc/nginx/nginx.conf
    sudo cp $nginx_proxy_file /etc/nginx/sites-available/virtual_env
    sudo ln -s /etc/nginx/sites-available/virtual_env /etc/nginx/sites-enabled/virtual_env
    sudo rm /etc/nginx/sites-enabled/default

# Step 5: Create the directories and clone the repositories
    # Manage website
    sudo mkdir -p /var/www/website
    sudo git clone $website_repo_url /var/www/website

    # Manage websocket server
    sudo mkdir -p /var/www/websocket
    sudo git clone $websocket_server_repo_url /var/www/websocket
    cd /var/www/website
    sudo $python -m venv venv
    source venv/bin/activate
    sudo pip install -r requirements.txt
    deactivate

    # Manage API server
    sudo mkdir -p /var/www/API
    sudo git clone $api_server_repo_url /var/www/API
    cd /var/www/API
    sudo $python -m venv venv
    source venv/bin/activate
    sudo pip install -r requirements.txt
    deactivate

# Step 6: Install supervisor
    sudo apt-get install supervisor -y

# Step 7: Configure supervisor
    sudo cp $supervisor_api_file /etc/supervisor/conf.d/api.conf
    sudo cp $supervisor_websocket_file /etc/supervisor/conf.d/websocket.conf

# Step 8: Install dnsmasq
    sudo apt-get install dnsmasq -y

# Step 9: Configure dnsmasq
    sudo cp $dnsmasq_conf_file /etc/dnsmasq.conf

# Step 10: Final configurations
    sudo rm -rf $script_path