import board
import adafruit_bmp280
import time
i2c = board.I2C()

while True:
	sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
	print('Temperature: {} ºC'.format(sensor.temperature)) 
	print('Pressure: {} hPa'.format(sensor.pressure))
	print('\n')
	time.sleep(1)
