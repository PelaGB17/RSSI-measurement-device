import adafruit_bmp280
import busio
import board

def inicializar_barometro():
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        barometer = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
        return barometer
    except Exception as e:
        print("Barometer disconnected:", e)
        return None

def obtener_datos_barometro(barometer):
    try:
        return barometer.pressure
    except:
        return None
