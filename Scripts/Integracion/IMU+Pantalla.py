import time
import math
import board
import busio
import adafruit_bmp280
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Configuracion del modulo de acelerometro, giroscopio y magnetometro (IMU)
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Configuracion de la pantalla SSD1306
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Crear un objeto de imagen para la pantalla OLED
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def obtener_datos_barometro():
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

    return (
        f"T:{sensor.temperature:.2f}\n"
        f"P:{sensor.pressure:.2f}\n"
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
            datos_barometro = obtener_datos_barometro()
            mostrar_datos_pantalla(datos_barometro)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
