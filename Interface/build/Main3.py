import argparse
import sys
import time
import os
import signal
from GNU_Radio import GNURadioBlock
from GPS import inicializar_gps, obtener_datos_gps
from Barometro import inicializar_barometro, obtener_datos_barometro
from Pantalla import inicializar_pantalla, mostrar_datos_pantalla
from Utilidades import obtener_distancia_gps, calcula_altitud, obtener_medidas, procesar_archivo, crear_siguiente_carpeta
import Heatmap
import Representacion

        
def main(top_block_cls=GNURadioBlock, lat_val=0, lon_val=0, p_val=1, f_val=0, g_val=20, n_val="medidas", options=None):
        self.status = True
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
                
                datos_gps = obtener_datos_gps()
                distancia = obtener_distancia_gps(lat_val, lon_val, datos_gps['latitude'], datos_gps['longitude'])
                presion = obtener_datos_barometro(self.barometro)
                altura = calcula_altitud(presion, p_val)
                mostrar_datos_pantalla(self.oled, datos_gps)
                timestamp = time.strftime("%H%M%S")
                           
                tb.wait()
                
                level=obtener_medidas(n_val)
                tb.stop()
                
                medidas= [f" {level}", f" {datos_gps['latitude']}", f" {datos_gps['longitude']}", f" {presion}", f" {distancia}", f"{altura}", f"{datos_gps['altitude']}" ,f"{timestamp}"]
                print(medidas)
                
                with open(ruta + "/" + n_val + ".txt", 'a') as txt_file:
                    txt_file.write(" ".join(medidas))
                    txt_file.write('\n')
                
                self.set_altitude(altura)
                self.set_longitude(datos_gps["longitude"])
                self.set_latitude(datos_gps["latitude"])
                self.set_RSSI(level)
                
                if self.status == False:
                    raise Exception("Measurement stopped")

            except Exception as e:
                print(e)
            finally:
                tb.stop()
                tb.wait()
                procesar_archivo(ruta, p_val, n_val)
                datos = ruta + n_val + ".txt"
                procesado = ruta + "procesado.txt"
                config = ruta + "config.txt"
                Heatmap.main(datos, ruta)
                Representacion.representa_medidas(procesado, config, ruta)
                os.remove(n_val)

def nivel_de_senal():
        top_block_cls=GNURadioBlock
        tb = top_block_cls(f_val=2400000000, g_val=40, n_val="medidas")
        
        def sig_handler(sig=None, frame=None):
            tb.stop()
            tb.wait()
            sys.exit(0)

        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
                
        tb.start()
        tb.wait()
        level=obtener_medidas("medidas")
        tb.stop()
        
        return level            

def create_info_file(freq_MHz=2400, g_tx=40, g_ant=0, h_tx=0.3, g_rx=40 ,h_rx=0.3, n_val="medidas"):
        if n_val == "medidas":
            ruta=crear_siguiente_carpeta("/home/rssidev/Desktop/Medidas", "a_prueba")
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
        return ruta
            

#if __name__ == '__main__':
#    parser = argparse.ArgumentParser(description='GNU Radio script.')
#    parser.add_argument('-lat', '--latitude', type=float, default=0, help='Input for latitude value')
#    parser.add_argument('-lon', '--longitude', type=float, default=0, help='Input for longitude value')
#    parser.add_argument('-p', '--pressure', type=float, default=1, help='Input for sea level pressure value')
#    parser.add_argument('-f', '--freq', type=float, default=2400000000, help='Input for frequency value')
#   parser.add_argument('-g', '--gain', type=float, default=40, help='Input for gain value')
#    parser.add_argument('-n', '--name', type=str, default="medidas", help='Input for name value')
#    args = parser.parse_args()
#    main(lat_val=args.latitude, lon_val=args.longitude, f_val=args.freq, p_val=args.pressure ,g_val=args.gain, n_val=args.name)
