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
import Scripts.Herramientas.Heatmap as Heatmap


def main(top_block_cls=GNURadioBlock, lat_val=0, lon_val=0, p_val=1, f_val=0, g_val=20, n_val="medidas", options=None):
    global ruta
    ruta=crear_siguiente_carpeta("/home/pelayo/Desktop/Medidas", "a_prueba")
    gps=inicializar_gps()
    oled=inicializar_pantalla()    
    barometro=inicializar_barometro()

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
            presion = obtener_datos_barometro(barometro)
            altura = calcula_altitud(presion, p_val)
            mostrar_datos_pantalla(oled, datos_gps)
            timestamp = time.strftime("%H:%M:%S")
                       
            tb.wait()
            
            level=obtener_medidas(n_val)
            tb.stop()
            
            medidas= [f" {level}", f" {datos_gps['latitude']}", f" {datos_gps['longitude']}", f" {presion}", f" {distancia}", f"{altura}", f"{timestamp}"]
            print(medidas)
            
            with open(ruta + "/" + n_val + ".txt", 'a') as txt_file:
                txt_file.write(" ".join(medidas))
                txt_file.write('\n')

        except KeyboardInterrupt:
            pass
        finally:
            tb.stop()
            tb.wait()
            procesar_archivo(ruta, p_val, n_val)
            Heatmap.main(ruta)
            os.remove(n_val)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GNU Radio script.')
    parser.add_argument('-lat', '--latitude', type=float, default=0, help='Input for latitude value')
    parser.add_argument('-lon', '--longitude', type=float, default=0, help='Input for longitude value')
    parser.add_argument('-p', '--pressure', type=float, default=1, help='Input for sea level pressure value')
    parser.add_argument('-f', '--freq', type=float, default=2400000000, help='Input for frequency value')
    parser.add_argument('-g', '--gain', type=float, default=40, help='Input for gain value')
    parser.add_argument('-n', '--name', type=str, default="medidas", help='Input for name value')
    args = parser.parse_args()
    main(lat_val=args.latitude, lon_val=args.longitude, f_val=args.freq, p_val=args.pressure ,g_val=args.gain, n_val=args.name)
