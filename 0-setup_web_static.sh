#!/usr/bin/env bash
# a script that sets up your web servers for the deployment of (web_static)

# installing nginx
if [ ! -x /usr/sbin/nginx ]
then
	sudo apt-get -y update
	sudo apt-get -y install nginx
fi

# create neede folders
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# creating fake html test file
echo 'Nginx is running correctly!' > /data/web_static/releases/test/index.html

# creating the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# changing owners
sudo chown -R ubuntu:ubuntu /data
sudo chmod -R 755 /data/

# updating nginx config
sudo sed -i '67 i \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# restarting nginx
sudo service nginx restart
