import argparse
import sys
import time
import os
import signal
from . import GNU_Radio, Utilidades

def nivel_de_senal():
        top_block_cls=GNU_Radio.GNURadioBlock
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

def create_info_file(freq_MHz=2400, g_tx=40, g_ant=0, h_tx=0.3, g_rx=40 ,h_rx=0.3, n_val="medidas"):
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
        return ruta
