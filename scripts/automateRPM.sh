#!/bin/bash
# Author: Jose Miguel Colella
# Description: Script creado para automatizar el proceso
# de instalar todo
cd ../

sudo yum update
sudo yum groupinstall -y "Development tools" --skip-broken

# Instalar web.py
sudo easy_install web.py
#Instalar lenguaje de templating
sudo easy_install mako
#Instalar driver para mongodb-server
sudo easy_install pymongo
#Instalar interfaz de twitter
sudo easy_install tweepy
# Instalar el feedparser
sudo easy_install feedparser

git clone https://github.com/josecolella/DAI_Practica4.git
cd DAI_Practica4
chmod +x index.py
# Para que el script siga ejecutando despues de que salga de ssh
sudo nohup ./index.py 80 &
