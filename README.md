# RSSI-measurement-device

### Materiales

- Raspberry Pi 4B
- Tarjeta Micro SD de al menos 12 GB
- Adaptador Micro SD a USB
- Ordenador

### Instalación de Raspberry Pi OS

Para realizar la instalación de Raspbian, es necesario descargar la imagen ISO de la página web oficial de Raspberry Pi: [Operating system images – Raspberry Pi](https://www.raspberrypi.org/software/operating-systems/). Para mayor compatibilidad, se empleará la versión de 64 bits con escritorio.

Posteriormente, se debe quemar la imagen en la tarjeta SD mediante un software dedicado, como Balena Etcher, Rufus o similar.

### Configuración del SO

Una vez flasheada la tarjeta, se introduce en la ranura de la Raspberry Pi y se enciende. Posteriormente, se realiza la configuración inicial de la Raspberry. Los directorios están pensados para utilizarse con el usuario “rssidev” y como contraseña puede utilizarse cualquiera. Es recomendable introducir la configuración WiFi; se puede usar cualquiera que se crea conveniente, siempre y cuando todos los dispositivos de control estén conectados a ella. En este caso, se ha configurado como SSID: “Raspberry.WLAN” y contraseña WPA2: “12345678”.

Cuando la Raspberry finalice de configurarse, antes de instalar programas, se deben activar las siguientes configuraciones. Para ello, se abre una terminal y se introduce el siguiente comando:

```
sudo raspi-config
```

Posteriormente, navegamos a `Interface options` y activamos las opciones de `SSH`, `VNC`, `I2C` y `Serial Port`. En la opción `Serial Port`, debemos activarla y decir que no cuando nos pregunte para habilitar Login Shell.

```
vncserver-virtual -RandR=1920x1080
```

Una vez cerrada la terminal, cambiaremos la resolución VNC para el dispositivo de control; en este caso, será de 1920x1080 px.

Antes de reiniciar, actualizaremos todos los componentes de la Raspberry Pi con los siguientes comandos:

```
sudo apt update
sudo apt upgrade
```

### Clonado del repositorio de GitHub

Todos los scripts necesarios para hacer funcionar el proyecto y los datos de las medidas tomadas se encuentran en el repositorio: [PelaGB17/RSSI-measurement-device](https://github.com/PelaGB17/RSSI-measurement-device). Para descargarlos, puede hacerse mediante el navegador o mediante Git. Mediante Git, es necesario instalarlo ejecutando el siguiente comando:

```
sudo apt install git
```

Una vez instalado Git, clonaremos el repositorio con el comando:

```
git clone https://github.com/PelaGB17/RSSI-measurement-device.git
```

Es importante ejecutar este comando en el directorio `/home/rssidev/` o sin haberse dirigido a otro directorio, ya que es relevante a la hora de instalar los programas y dependencias.

### Instalación de programas y dependencias

Con la finalidad de simplificar la instalación de dependencias, se ha hecho un script para ejecutar con la terminal, para poder instalar de forma sencilla todos los componentes necesarios. El script se encuentra en el repositorio de GitHub en la ubicación `Scripts/Herramientas` con el nombre “Dependencias.sh”.

### Funcionamiento del programa

Previamente al inicio del programa, debemos iniciar gpsd. Para ello, debemos usar el siguiente comando:

```
sudo gpsd -D3 -N /dev/ttyS0 ntrip://usuario@servidor/punto_de_montaje
```

Una vez instalado el programa y las dependencias, existen dos formas de utilizar el programa:

```
1. sudo rssidev-cli
2. sudo rssidev-gui
```

El comando (1) lanzará el programa sin interfaz gráfica, de modo que el programa irá pidiendo al usuario los parámetros necesarios para el funcionamiento.

El comando (2) lanzará el programa con la siguiente interfaz gráfica:

Al presionar el botón “Test”, el programa lanzará una única lectura de los parámetros, con la finalidad de controlar que todos los sensores y la USRP están funcionando correctamente.

Al presionar el botón “Inicio”, con los campos de configuración previamente rellenados, el programa leerá dichos campos y comenzará su ejecución hasta que el usuario salga del programa con la tecla “Esc” o presione el botón Stop.

### Obtención de los archivos

Una vez finalizadas las medidas, el usuario puede extraer las medidas de la Raspberry Pi de dos formas simples:

1. Mediante un lápiz USB, las medidas están almacenadas en el Escritorio, dentro de una carpeta con el nombre de Medidas.
2. Mediante el protocolo FTP, el cual debe estar previamente configurado. En caso de no estarlo, a continuación se describen los pasos:

   - Se introduce en la consola:

     ```
     sudo apt install vsftpd
     ```

   - Una vez instalado el programa, es necesario editar los parámetros de configuración del servicio FTP mediante el comando:

     ```
     sudo nano /etc/vsftpd.conf
     ```

   - Debemos cambiar la línea de `anonymous_enable = NO` a `anonymous_enable = YES` y quitar el comentario de la línea `write_enable = YES`.

   - Posteriormente, debemos añadir permisos en el escritorio con el comando:

     ```
     sudo chmod -777 -R /Desktop
     ```

   - Finalmente, establecemos el servicio FTP para que comience a funcionar y a que se inicie al encender la Raspberry con los comandos:

     ```
     sudo systemctl start vsftpd
     sudo systemctl enable vsftpd
     ```
