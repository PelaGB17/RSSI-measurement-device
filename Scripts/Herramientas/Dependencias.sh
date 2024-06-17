#!/bin/bash

# Actualiza la lista de paquetes disponibles dos veces
sudo apt update && sudo apt update

# Inicia el servidor VNC virtual con una resolucion de 1920x1080
vncserver-virtual -RandR=1920x1080

# Instala GNU Radio
sudo apt-get install -y gnuradio

# Instala las dependencias de UHD
sudo apt-get install -y libuhd-dev uhd-host

# Descarga las imagenes de UHD
sudo uhd_images_downloader

# Instala Visual Studio Code
sudo apt install -y code

# Instala los programas con y sin interfaz
sudo pip install /home/rssidev/RSSI-measurement-device/Programa_V2_gui/dist/RSSI_measurement_device_interfaced-0.0.2-py3-none-any.whl --break-system-packages

sudo pip install /home/rssidev/RSSI-measurement-device/Programa_V2/dist/RSSI_measurement_device-0.0.2-py3-none-any.whl --break-system-packages

mkdir /Desktop/Medidas

# Instala gpsd
sudo apt install -y scons libncurses-dev pps-tools git-core asciidoctor python3-matplotlib build-essential manpages-dev pkg-config python3-distutils

wget http://download.savannah.gnu.org/releases/gpsd/gpsd-3.25.tar.gz

tar -xzf gpsd-3.25.tar.gz

cd gpsd-3.25/

sudo scons

sudo scons install

sudo reboot