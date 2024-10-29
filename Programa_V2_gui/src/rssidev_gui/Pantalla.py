import adafruit_ssd1306
import busio
import board
from PIL import Image, ImageDraw, ImageFont
from . import Utilidades

def inicializar_pantalla():
    try:
        # Initialize the screen object
        screen = {}

        i2c = busio.I2C(board.SCL, board.SDA)
        screen["oled"] = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        
        # Create an image object for the OLED screen
        screen["image"] = Image.new("1", (screen["oled"].width, screen["oled"].height))
        screen["draw"] = ImageDraw.Draw(screen["image"])
        screen["font"] = ImageFont.load_default()

        # Configuration of the grid
        screen["GRID_SIZE"] = 10
        screen["GRID_COLOR"] = 255

        # Initialize central position
        screen["central_longitude"] = None
        screen["central_latitude"] = None
        screen["first_coordinate_received"] = False

        # Store points
        screen["stored_points"] = []
        
        return screen
    except Exception as e:
        print("Screen disconnected:", e)
        return None


def mostrar_datos_pantalla(display, data):
    try:
        # Clear the image
        display["draw"].rectangle((0, 0, display["oled"].width, display["oled"].height), outline=0, fill=0)

        # Draw grid
        for x in range(0, display["oled"].width, display["oled"].width // display["GRID_SIZE"]):
            display["draw"].line((x, 0, x, display["oled"].height), fill=display["GRID_COLOR"])
        for y in range(0, display["oled"].height, display["oled"].height // display["GRID_SIZE"]):
            display["draw"].line((0, y, display["oled"].width, y), fill=display["GRID_COLOR"])

        # If it's the first coordinate, center the screen
        if not display["first_coordinate_received"]:
            display["central_longitude"] = data["longitude"]
            display["central_latitude"] = data["latitude"]
            display["first_coordinate_received"] = True

        # Calculate distance in meters from the central position
        dist_lat = Utilidades.obtener_distancia_gps(display["central_latitude"], display["central_longitude"], data["latitude"], display["central_longitude"])
        dist_lon = Utilidades.obtener_distancia_gps(display["central_latitude"], display["central_longitude"], display["central_latitude"], data["longitude"])

        # Convert distances to pixels and store in list
        x = int((dist_lon + 100) * (display["oled"].width / 200))
        y = int((dist_lat + 50) * (display["oled"].height / 100))
        display["stored_points"].append((x, y))

        # Draw stored points
        for px, py in display["stored_points"]:
            display["draw"].rectangle((px - 1, py - 1, px + 1, py + 1), outline=255, fill=255)

        display["oled"].image(display["image"])
        display["oled"].show()
        
    except Exception as e:
        print("Error drawing data on display:", e)


