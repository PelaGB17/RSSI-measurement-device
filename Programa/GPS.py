import gpsd
import time

def inicializar_gps():
    try:
        gpsd.connect()
        return "Correct"

    except Exception as e:
        print("GPS disconnected:", e)
        return None

def obtener_datos_gps():
    try:
        packet = gpsd.get_current()
        
        if packet.mode < 2 or packet.lat == 0.0:
            packet = gpsd.get_current()
            print("GPS is not having valid data")
            return {
            "longitude": None,
            "latitude": None,
            "speed_knots": None,
            "satellites": None,
            "altitude": None,
        }
        
        alt = None
        
        if packet.mode >= 3:
            alt = packet.alt,
            
        return {
            "longitude": packet.lon,
            "latitude": packet.lat,
            "speed_knots": packet.hspeed,
            "satellites": packet.sats,
            "altitude": alt,
        }
        
    except Exception as e:
        print("Error getting GPS data:", e)
        return {
            "longitude": None,
            "latitude": None,
            "speed_knots": None,
            "satellites": None,
            "altitude": None,
        }
