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
uhd_images_downloader

# Instala Git
sudo apt install -y git

# Instala Visual Studio Code
sudo apt install -y code

# Instala los programas con y sin interfaz
sudo pip install RSSI-measurement-device/Programa_V2_gui/dist/rssi_measurement_device_interfaced-0.0.2.whl --break-system-packages

sudo pip install RSSI-measurement-device/Programa_V2/dist/rssi_measurement_device-0.0.2.whl --break-system-packages