#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: test_RSSI_file
# GNU Radio version: 3.9.0.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time

import argparse

import adafruit_gps
import serial
import sys
import busio
import board
import numpy
import adafruit_ssd1306
import adafruit_bmp280
import gpsd
from PIL import Image, ImageDraw, ImageFont
from geopy.distance import geodesic

# Conectar al GPS
gpsd.connect()
packet = gpsd.get_current()

# Configuracion de la pantalla SSD1306 y el barómetro
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
barometro = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Crear un objeto de imagen para la pantalla OLED
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Configuracion de la cuadricula
GRID_SIZE = 10
GRID_COLOR = 255

# Inicializar la posición central
central_longitude = None
central_latitude = None
first_coordinate_received = False

# Almacenar puntos
stored_points = []


class test_RSSI_file(gr.top_block):

    def __init__(self, f_val = 0, g_val = 20, n_val = "medidas"):
        gr.top_block.__init__(self, "test_RSSI_file", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.gain_rx = gain_rx = g_val
        self.fm = fm = 100e3
        self.file = file = n_val
        self.fc = fc = f_val
    


        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("serial=31BA199", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0_0.set_center_freq(fc, 0)
        self.uhd_usrp_source_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0_0.set_gain(gain_rx, 0)
        self.uhd_usrp_source_0_0.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source_0_0.set_auto_iq_balance(False, 0)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_float*1, (1, 1))
        self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_float*1, int(samp_rate))
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, int(samp_rate))
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(int(samp_rate), 1/samp_rate, 4000, 1)
        self.blocks_head_0 = blocks.head(gr.sizeof_float*1, 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, file, True)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.band_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                fm - 50e3,
                fm + 50e3,
                100e3,
                window.WIN_HAMMING,
                6.76))
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_skiphead_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_skiphead_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_skiphead_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, self.fm - 50e3, self.fm + 50e3, 100e3, window.WIN_HAMMING, 6.76))
        self.blocks_moving_average_xx_0_0.set_length_and_scale(int(self.samp_rate), 1/self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

    def get_gain_rx(self):
        return self.gain_rx

    def set_gain_rx(self, gain_rx):
        self.gain_rx = gain_rx
        self.uhd_usrp_source_0_0.set_gain(self.gain_rx, 0)

    def get_fm(self):
        return self.fm

    def set_fm(self, fm):
        self.fm = fm
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, self.fm - 50e3, self.fm + 50e3, 100e3, window.WIN_HAMMING, 6.76))

    def get_file(self):
        return self.file

    def set_file(self, file):
        self.file = file
        self.blocks_file_sink_0.open(self.file)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.uhd_usrp_source_0_0.set_center_freq(self.fc, 0)

def obtener_distancia_gps(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).meters

def obtener_datos_gps():
    packet = gpsd.get_current()
    while packet.mode<2 or packet.lat==0.0:
                packet = gpsd.get_current()
                time.sleep(1)
                print("GPS is not having valid data")
    alt=None
    if packet.mode>=3:
        alt=packet.alt,
    return {
        "longitude": packet.lon,
        "latitude": packet.lat,
        "speed_knots": packet.hspeed,
        "satellites": packet.sats,
        "altitude": alt,
    }

def obtener_datos_barometro():
    barometro = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    return barometro.pressure
    
def obtener_medidas(n_val):
    # Obtiene las mediciones de GNURadio del archivo binario
    with open(n_val, 'rb') as bin_file:
        f = numpy.fromfile(bin_file, dtype=numpy.float32)
            
    # Formatea la medicion de GNURadio
    for i in range(0, len(f), 2):
        level=str(f[i])
    return level
    
    #Borra la línea del archivo binario
    with open(n_val, 'w') as file:
        file.truncate(0)

def mostrar_datos_pantalla(datos):
    global central_longitude, central_latitude, first_coordinate_received

    # Borrar la imagen
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Dibujar cuadricula
    for x in range(0, oled.width, oled.width // GRID_SIZE):
        draw.line((x, 0, x, oled.height), fill=GRID_COLOR)
    for y in range(0, oled.height, oled.height // GRID_SIZE):
        draw.line((0, y, oled.width, y), fill=GRID_COLOR)

    # Si es la primera coordenada, centrar la pantalla
    if not first_coordinate_received:
        central_longitude = datos["longitude"]
        central_latitude = datos["latitude"]
        first_coordinate_received = True

    # Calcular la distancia en metros desde la posición central
    dist_lat = obtener_distancia_gps(central_latitude, central_longitude, datos["latitude"], central_longitude)
    dist_lon = obtener_distancia_gps(central_latitude, central_longitude, central_latitude, datos["longitude"])

    # Convertir las distancias a píxeles y guardado en lista
    x = int((dist_lon + 100) * (oled.width / 200))
    y = int((dist_lat + 50) * (oled.height / 100))
    stored_points.append((x, y))

    #Dibujar puntos almacenados
    for px, py in stored_points:
         draw.rectangle((px - 1, py - 1, px + 1, py + 1), outline=255, fill=255)

    oled.image(image)
    oled.show()
    
def crear_siguiente_carpeta(directorio_base, nombre_base):
    # Obtener una lista de nombres de todas las subcarpetas
    subcarpetas = [nombre for nombre in os.listdir(directorio_base) if os.path.isdir(os.path.join(directorio_base, nombre))]

    # Encontrar el número más alto y calcular el nombre para la siguiente carpeta
    numeros = [int(nombre.split('_')[0]) for nombre in subcarpetas if nombre.startswith(nombre_base)]
    if numeros:
        siguiente_numero = max(numeros) + 1
    else:
        siguiente_numero = 1

    nuevo_nombre = f"{siguiente_numero}{nombre_base}"

    # Crear la nueva carpeta
    nueva_ruta = os.path.join(directorio_base, nuevo_nombre)
    os.mkdir(nueva_ruta)

    return nueva_ruta
    
def calcula_altitud(presion, presion_nivel_mar) -> float:
            """The altitude based on the sea level pressure (:attr:`sea_level_pressure`)
            - which you must enter ahead of time)"""
            p = presion # in Si units for hPascal
            return 44330 * (1.0 - math.pow(p / presion_nivel_mar, 0.1903))+30
    
def procesar_archivo(path, presion_nivel_mar):
        with open(path, 'r') as input_file:
            lines = input_file.readlines()

        with open(path, 'w') as output_txt_file:
            for line in lines:
                columns = line.split()
                output_txt_file.write(f"{columns[0]} {columns[4]}\n")
                
        kml_header = """<?xml version="1.0" encoding="UTF-8"?>
                    <kml xmlns="http://www.opengis.net/kml/2.2">
                      <Document>
                        <name>Medidas en Google Maps</name>
                        <description>Coordenadas con medidas</description>
                    """

        kml_footer = """    </Document>
                    </kml>
                    """

        kml_placemark_template = """
                        <Placemark>
                          <name>{name}</name>
                          <Point>
                            <coordinates>{longitude},{latitude},{altitude}</coordinates>
                          </Point>
                          <ExtendedData>
                            <Data name="Measure">
                              <value>{measure}</value>
                            </Data>
                          </ExtendedData>
                        </Placemark>
                    """
        kml_body = ""
        
        for i, line in enumerate(lines):
            data = line.split()
            name = f"Medida_{i + 1}"
            kml_body += kml_placemark_template.format(name=name, measure=data[0], longitude=data[2], latitude=data[1], altitude=calcula_altitud(float(data[3]),presion_nivel_mar))

        with open(path, 'w') as kml_file:
            kml_file.write(kml_header + kml_body + kml_footer)


def main(top_block_cls=test_RSSI_file, lat_val=0, lon_val=0, p_val=0, f_val=0, g_val=20, n_val="medidas", options=None):

    def sig_handler(sig=None, frame=None, tb=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    
    ruta=crear_siguiente_carpeta("/home/pelayo/Desktop/Medidas", "a_prueba"):

    while True:
        tb = top_block_cls(f_val=f_val, g_val=g_val, n_val=n_val)
        try:
            tb.start()
            
            datos_gps = obtener_datos_gps()
            distancia = obtener_distancia_gps(lat_val, lon_val, datos_gps['latitude'], datos_gps['longitude'])
            presion = obtener_datos_barometro()
            mostrar_datos_pantalla(datos_gps)
                       
            tb.wait()
            
            level=obtener_medidas(n_val)
            
            medidas= [f" {level}", f" {datos_gps['latitude']}", f" {datos_gps['longitude']}", f" {presion}", f" {distancia}"]
            print(medidas)
            
            with open(ruta + n_val + ".txt", 'a') as txt_file:
                txt_file.write(" ".join(medidas))
                txt_file.write('\n')
                                     
            tb.stop()
            time.sleep(1)

        except KeyboardInterrupt:
            pass
        finally:
            procesar_archivo(ruta + n_val + ".txt")
            tb.stop()
            tb.wait()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GNU Radio script.')
    parser.add_argument('-lat', '--latitude', type=float, default=0, help='Input for latitude value')
    parser.add_argument('-lon', '--longitude', type=float, default=0, help='Input for longitude value')
    parser.add_argument('-p', '--pressure', type=float, default=0, help='Input for sea level pressure value')
    parser.add_argument('-f', '--freq', type=float, default=0, help='Input for frequency value')
    parser.add_argument('-g', '--gain', type=float, default=20, help='Input for gain value')
    parser.add_argument('-n', '--name', type=str, default="medidas", help='Input for name value')
    args = parser.parse_args()
    main(lat_val=args.latitude, lon_val=args.longitude, f_val=args.freq, p_val=args.pressure ,g_val=args.gain, n_val=args.name)

