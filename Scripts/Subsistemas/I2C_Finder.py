import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
devices = i2c.scan()
print("Dispositivos I2C encontrados:", [hex(device) for device in devices])
