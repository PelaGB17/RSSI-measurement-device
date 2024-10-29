import time
import board
import busio
import serial
import adafruit_gps
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Configuraci�n del m�dulo GPS
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart)

# Configuraci�n de la pantalla SSD1306
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Crear un objeto de imagen para la pantalla OLED
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def obtener_datos_gps():
    return (
       #  f"LAT: {gps.latitude}\n"
        f"LNG: {gps.longitude}\n"
        f"Speed: {gps.speed_knots} knots\n"
        f"SAT: {gps.satellites}\n"
        f"ALT: {gps.altitude_m}"
    )

def mostrar_datos_pantalla(datos):
    # Borrar la imagen antes de escribir nuevos datos
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    draw.text((0, 0), datos, font=font, fill=255)
    oled.image(image)
    oled.show()

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
