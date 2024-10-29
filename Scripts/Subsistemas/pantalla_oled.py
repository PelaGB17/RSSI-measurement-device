import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont
import socket
import fcntl
import struct
import subprocess

# Funcion para obtener la direccion IP de una interfaz
def obtener_direccion_ip(interface):
    try:
        ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        direccion_ip = socket.inet_ntoa(fcntl.ioctl(
            ip_socket.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', interface[:15].encode('utf-8'))
        )[20:24])
        return direccion_ip
    except IOError:
        return "No disponible"

# Funcion para obtener el nombre de la red de una interfaz WLAN
def obtener_nombre_red(interface):
    try:
        result = subprocess.check_output(['iwgetid', interface])
        nombre_red = result.decode().split('"')[1]
        return nombre_red
    except subprocess.CalledProcessError:
        return "No disponible"

# Configuracion del display OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 32, i2c)

# Limpia la pantalla OLED
oled.fill(0)
oled.show()
# Rotacion de la pantalla en 180 grados
oled.rotation = 0  # Esto gira la pantalla 180 grados (0, 1, 2 o 3 para diferentes rotaciones)


# Crea un objeto Image con fondo negro
imagen = Image.new("1", (oled.width, oled.height))
dibujo = ImageDraw.Draw(imagen)

# Carga una fuente predeterminada
fuente = ImageFont.load_default()
# Especifica la ruta de la fuente TrueType (TTF)
ruta_fuente = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Ruta de ejemplo, cambia segun tu fuente

# Carga la fuente TrueType (TTF) con el tamaño y el estilo que desees
fuente = ImageFont.truetype(ruta_fuente, 10)

# Obtener el nombre del SSID del punto de acceso
nombre_ssid = obtener_nombre_red("wlan0")
# Mostrar el nombre del SSID y su IP en la pantalla OLED
dibujo.text((0, 0), f"{nombre_ssid}", font=fuente, fill=255)
# Obtener la direccion IP de la interfaz wlan0
ip_wlan0 = obtener_direccion_ip("wlan0")
# Mostrar la IP de wlan0 en la pantalla OLED
dibujo.text((0, 10), f"IP: {ip_wlan0}", font=fuente, fill=255)

# Si esta conectada la interfaz wwan0, mostrar su IP
ip_wwan0 = obtener_direccion_ip("wwan0")
if ip_wwan0 != "No disponible":
    dibujo.text((0, 0), f"Conexion 5G", font=fuente, fill=255)
    dibujo.text((0, 10), f"IP: {ip_wwan0}", font=fuente, fill=255)

# Obtener el nombre de la red de la interfaz WLAN1 y su IP
nombre_red_wlan1 = obtener_nombre_red("wlan1")
ip_wlan1 = obtener_direccion_ip("wlan1")
# Mostrar el nombre de la red y su IP en la pantalla OLED
dibujo.text((0, 20), f"StarG Relay: {ip_wlan1}", font=fuente, fill=255)

# Muestra la imagen en la pantalla OLED
oled.image(imagen)
oled.show()
