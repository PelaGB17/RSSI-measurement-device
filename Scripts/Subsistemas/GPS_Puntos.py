import time
import board
import busio
import serial
import adafruit_gps
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from geopy.distance import geodesic

# Configuracion del modulo GPS
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart)

# Configuracion de la pantalla SSD1306
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Crear un objeto de imagen para la pantalla OLED
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Configuracion de la cuadricula
GRID_SIZE = 10
GRID_COLOR = 255  # Blanco

# Inicializar la posición central
central_longitude = None
central_latitude = None
first_coordinate_received = False

# Almacenar puntos
stored_points = []

def obtener_distancia(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).meters

def obtener_datos_gps():
    return {
        "longitude": gps.longitude,
        "latitude": gps.latitude,
        "speed_knots": gps.speed_knots,
        "satellites": gps.satellites,
        "altitude_m": gps.altitude_m,
    }

def mostrar_datos_pantalla(datos):
    global central_longitude, central_latitude, first_coordinate_received

    # Borrar la imagen antes de dibujar la cuadricula y los puntos
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Dibujar cuadricula
    for x in range(0, oled.width, oled.width // GRID_SIZE):
        draw.line((x, 0, x, oled.height), fill=GRID_COLOR)
    for y in range(0, oled.height, oled.height // GRID_SIZE):
        draw.line((0, y, oled.width, y), fill=GRID_COLOR)

    # Verificar si hay una fijacion GPS valida
    if datos["longitude"] is not None and datos["latitude"] is not None:
        # Si es la primera coordenada, centrar la pantalla
        if not first_coordinate_received:
            central_longitude = datos["longitude"]
            central_latitude = datos["latitude"]
            first_coordinate_received = True

        # Calcular la distancia en metros desde la posición central
        dist_lat = obtener_distancia(
            central_latitude, central_longitude, datos["latitude"], central_longitude
        )
        dist_lon = obtener_distancia(
            central_latitude, central_longitude, central_latitude, datos["longitude"]
        )

        # Convertir las distancias a píxeles
        x = int((dist_lon + 100) * (oled.width / 200))
        y = int((dist_lat + 50) * (oled.height / 100))

        # Almacenar el punto en la lista
        stored_points.append((x, y))

        # Dibujar puntos almacenados más grandes
        for px, py in stored_points:
            draw.rectangle((px - 2, py - 2, px + 2, py + 2), outline=255, fill=255)

    oled.image(image)
    oled.show()
    
    print("Satélites encontrados: " + str(datos["satellites"]))

def main():
    try:
        while True:
            gps.update()
            datos_gps = obtener_datos_gps()
            mostrar_datos_pantalla(datos_gps)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
