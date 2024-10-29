import sys
import time
import os
import signal
from . import GNU_Radio, GPS, Barometro, Pantalla, Utilidades, Representacion, Heatmap

class Main:
    def __init__(self):
        GPS.inicializar_gps()
        self.oled = Pantalla.inicializar_pantalla()
        self.barometro = Barometro.inicializar_barometro()

    def obtener_calibracion(g_val = 40, f_val = 2.4e9):
        Ganancia_rx = [
        [10.91, -5.89, -14.8, -26.30],
        [14.17, -0.23, -10.77, -18.02],
        [9.93, -7.09, -16.6, -26.05],
        [15.38, -0.25, -8.9, -17.5]
        ]

        if g_val == 0:
            if f_val == 2.3e3 or f_val == 2.4e3:
                cal_off = Ganancia_rx[2][0]
            else:
                cal_off = Ganancia_rx[3][0]
        elif g_val == 20:
            if f_val == 2.3e3 or f_val == 2.4e3:
                cal_off = Ganancia_rx[2][1]
            else:
                cal_off = Ganancia_rx[3][1]
        elif g_val == 30:
            if f_val == 2.3e3 or f_val == 2.4e3:
                cal_off = Ganancia_rx[2][2]
            else:
                cal_off = Ganancia_rx[3][2]
        else:
            if f_val == 2.3e3 or f_val == 2.4e3:
                cal_off = Ganancia_rx[2][3]
            else:
                cal_off = Ganancia_rx[3][3]
        
        return cal_off + 6
        
    def main(self, top_block_cls=GNU_Radio.GNURadioBlock, lat_val=0, lon_val=0, p_val=1, f_val=0, g_val=20, n_val="medidas", options=None):
        self.status = True
        self.cal_off = self.obtener_calibracion(g_val, f_val)
        while True:
            tb = top_block_cls(f_val=f_val, g_val=g_val, n_val=n_val)
            try:
                def sig_handler(sig=None, frame=None):
                    tb.stop()
                    tb.wait()
                    sys.exit(0)

                signal.signal(signal.SIGINT, sig_handler)
                signal.signal(signal.SIGTERM, sig_handler)
                
                tb.start()
                
                datos_gps = GPS.obtener_datos_gps()
                distancia = Utilidades.obtener_distancia_gps(lat_val, lon_val, datos_gps['latitude'], datos_gps['longitude'])
                presion = Barometro.obtener_datos_barometro(self.barometro)
                altura = Utilidades.calcula_altitud(presion, p_val)
                Pantalla.mostrar_datos_pantalla(self.oled, datos_gps)
                timestamp = time.strftime("%H%M%S")
                           
                tb.wait()
                
                level=Utilidades.obtener_medidas(n_val)
                real_level = level + self.cal_off
                tb.stop()
                
                medidas= [f" {level}", f" {datos_gps['latitude']}", f" {datos_gps['longitude']}", f" {presion}", f" {distancia}", f"{altura}", f"{datos_gps['altitude']}" ,f"{timestamp}", f"{real_level}"]
                print(medidas)
                
                with open(ruta + "/" + "medidas.txt", 'a') as txt_file:
                    txt_file.write(" ".join(medidas))
                    txt_file.write('\n')
                

            except Exception as e:
                print(e)
                Utilidades.procesar_archivo(ruta, p_val, n_val)
                datos = ruta + "medidas.txt"
                procesado = ruta + "procesado.txt"
                config = ruta + "config.txt"
                Heatmap.main(datos, ruta)
                Representacion.representa_medidas(procesado, config, ruta)
                os.remove(n_val)
            finally:
                tb.stop()
                tb.wait()
                os.remove(n_val)

    def nivel_de_senal(self):
        top_block_cls=Utilidades.GNURadioBlock
        tb = top_block_cls(f_val=2400000000, g_val=40, n_val="medidas")
        
        def sig_handler(sig=None, frame=None):
            tb.stop()
            tb.wait()
            sys.exit(0)

        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
                
        tb.start()
        tb.wait()
        level=Utilidades.obtener_medidas("medidas")
        tb.stop()
        
        return level            

    def create_info_file(self, freq_MHz=2400, g_tx=40, g_ant=0, h_tx=0.3, g_rx=40 ,h_rx=0.3, n_val="medidas"):
        global ruta
        if n_val == "medidas":
            ruta=Utilidades.crear_siguiente_carpeta("/home/rssidev/Desktop/Medidas", "a_prueba")
        else:
            ruta=os.path.join("/home/rssidev/Desktop/Medidas/",n_val)
            os.mkdir(ruta)
        with open(ruta + "/" + "config" + ".txt", 'w') as txt_file:
            txt_file.write("% Line 1: Frecuencia de operación (MHz). Los posibles valores son únicamente 2.3e3 ó 5.1e3 MHz.\n")
            txt_file.write("% Line 2: Ganancia Tx (dB).  Los posibles valores son entre 0 y 80 dB con pasos de 10 dB.\n")
            txt_file.write("% Line 3: Ganancia de las antenas (dB).\n")
            txt_file.write("% Line 4: Altura de las antenas Tx (m).\n")
            txt_file.write("% Line 5: Ganancia Rx (dB). Los posibles valores son entre 0 y 80 dB con pasos de 10 dB.\n")
            txt_file.write("% Line 6: Altura de las antenas Rx (m).\n")
            txt_file.write(str(freq_MHz) + "\n")
            txt_file.write(str(g_tx) + "\n")
            txt_file.write(str(g_ant) + "\n")
            txt_file.write(str(h_tx) + "\n")
            txt_file.write(str(g_rx) + "\n")
            txt_file.write(str(h_rx) + "\n")
            
    def set_RSSI(self, RSSI):
        self.interfaz.set_RSSI(RSSI)
        
    def set_altitude(self, altitude):
        self.interfaz.set_altitude(altitude)
    
    def set_latitude(self, latitude):
        self.interfaz.set_latitude(latitude)
        
    def set_longitude(self, longitude):
        self.interfaz.set_longitude(longitude)

if __name__ == '__main__':
    freq = float(input("Introduzca la frecuencia de operación (GHz): "))
    g_rx = int(input("Introduzca la ganancia del receptor (dB): "))
    g_tx = int(input("Introduzca la ganancia del transmisor (dB): "))
    lat = float(input("Introduzca la latitud del transmisor (º): "))
    lon = float(input("Introduzca la longitud del transmisor (º): "))
    h_tx = float(input("Introduzca la altura del transmisor (m): "))
    h_rx = float(input("Introduzca la altura del receptor (m): "))
    pres = float(input("Introduzca la presión atmosférica a nivel del mar (hPa): "))
    g_ant = int(input("Introduzca la ganancia de las antenas (dB): "))
    name = input("Introduzca el nombre de la medida (dB): ")
    freq_Hz=freq*1e9
    freq_MHz=freq*1e3
    m = Main()
    m.create_info_file(freq_MHz=freq_MHz, g_tx=g_tx, g_ant=g_ant, h_tx=h_tx, g_rx=g_rx ,h_rx=h_rx, n_val=name)
    m.main(lat_val=lat, lon_val=lon, p_val=pres, f_val=freq, g_val=g_rx, n_val=name)

def start():
    freq = float(input("Introduzca la frecuencia de operación (GHz): "))
    g_rx = int(input("Introduzca la ganancia del receptor (dB): "))
    g_tx = int(input("Introduzca la ganancia del transmisor (dB): "))
    lat = float(input("Introduzca la latitud del transmisor (º): "))
    lon = float(input("Introduzca la longitud del transmisor (º): "))
    h_tx = float(input("Introduzca la altura del transmisor (m): "))
    h_rx = float(input("Introduzca la altura del receptor (m): "))
    pres = float(input("Introduzca la presión atmosférica a nivel del mar (hPa): "))
    g_ant = int(input("Introduzca la ganancia de las antenas (dB): "))
    name = input("Introduzca el nombre de la medida (dB): ")
    freq_Hz=freq*1e9
    freq_MHz=freq*1e3
    m = Main()
    m.create_info_file(freq_MHz=freq_MHz, g_tx=g_tx, g_ant=g_ant, h_tx=h_tx, g_rx=g_rx ,h_rx=h_rx, n_val=name)
    m.main(lat_val=lat, lon_val=lon, p_val=pres, f_val=freq_Hz, g_val=g_rx, n_val=name)