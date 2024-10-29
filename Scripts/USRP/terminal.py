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
from PIL import Image, ImageDraw, ImageFont
from geopy.distance import geodesic

#Configuracion del puerto serial para el módulo GPS
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)

# Configuracion de la pantalla SSD1306
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Crear un objeto de imagen para la pantalla OLED
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Configuracion de la cuadricula
GRID_SIZE = 10
GRID_COLOR = 255  # Blanco

# Inicializar la posición central
central_longitude = None
central_latitude = None
first_coordinate_received = False

# Almacenar puntos
stored_points = []


class test_RSSI_file(gr.top_block):

    def __init__(self, d_val = -5, f_val = 0, g_val = 20, n_val = "medidas"):
        gr.top_block.__init__(self, "test_RSSI_file", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.gain_rx = gain_rx = g_val
        self.fm = fm = 100e3
        self.file = file = n_val
        self.fc = fc = f_val
        self.distance = distance = d_val
    


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
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, distance)



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

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance
        self.analog_const_source_x_0.set_offset(self.distance)

def obtener_distancia(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).meters

def obtener_datos_gps():
    return {
        "longitude": gps.longitude,
        "latitude": gps.latitude,
        "longitude_d": gps.longitude_degrees,
        "longitude_m": gps.longitude_minutes,
        "latitude_d": gps.latitude_degrees,
        "latitude_m": gps.latitude_minutes,
        "speed_knots": gps.speed_knots,
        "satellites": gps.satellites,
        "altitude_m": gps.altitude_m,
    }


def mostrar_datos_pantalla(datos):
    global central_longitude, central_latitude, first_coordinate_received

    # Borrar la imagen antes de dibujar la cuadricula y los puntos
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Dibujar cuadricula
    for x in range(0, oled.width, oled.width // GRID_SIZE):
        draw.line((x, 0, x, oled.height), fill=GRID_COLOR)
    for y in range(0, oled.height, oled.height // GRID_SIZE):
        draw.line((0, y, oled.width, y), fill=GRID_COLOR)

    # Verificar si hay una fijacion GPS valida
    if datos["longitude"] is not None and datos["latitude"] is not None:
        # Si es la primera coordenada, centrar la pantalla
        if not first_coordinate_received:
            central_longitude = datos["longitude"]
            central_latitude = datos["latitude"]
            first_coordinate_received = True

        # Calcular la distancia en metros desde la posición central
        dist_lat = obtener_distancia(
            central_latitude, central_longitude, datos["latitude"], central_longitude
        )
        dist_lon = obtener_distancia(
            central_latitude, central_longitude, central_latitude, datos["longitude"]
        )

        # Convertir las distancias a píxeles
        x = int((dist_lon + 100) * (oled.width / 200))
        y = int((dist_lat + 50) * (oled.height / 100))

        # Almacenar el punto en la lista
        stored_points.append((x, y))

        # Dibujar puntos almacenados más grandes
        for px, py in stored_points:
            draw.rectangle((px - 1, py - 1, px + 1, py + 1), outline=255, fill=255)

    oled.image(image)
    oled.show()

def main(top_block_cls=test_RSSI_file, d_val=-5, f_val=0, g_val=20, n_val="medidas", options=None):

    def sig_handler(sig=None, frame=None, tb=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    while True:
        tb = top_block_cls(d_val=d_val, f_val=f_val, g_val=g_val, n_val=n_val)
        try:
            tb.start()
            
            gps.update()
            
            while not gps.has_fix:
                gps.update()
                time.sleep(1)
                print("GPS is not having fix")
            
            datos_gps = obtener_datos_gps()
            mostrar_datos_pantalla(datos_gps)
            
            latitude_d = datos_gps["latitude_d"]
            longitude_d = datos_gps["longitude_d"]
            latitude_m = datos_gps["latitude_m"]
            longitude_m = datos_gps["longitude_m"]
            altitude = datos_gps["altitude_m"]
            satellites = datos_gps["satellites"]
           
            tb.wait()
            
            # Obtiene las mediciones de GNURadio
            with open(n_val, 'rb') as bin_file:
                f = numpy.fromfile(bin_file, dtype=numpy.float32)
            
            # Formatea las mediciones de GNURadio
            for i in range(0, len(f), 2):
                level=str(f[i])
                distance=str(f[i+1])

            # Imprime la latitud y longitud
            print("Level:", level, "Latitude degrees:", latitude_d, "Latitude minutes:", latitude_m,"Longitude degrees:", longitude_d, "Longitude minutes:", longitude_m,"Altitude: ", altitude, "Satellites:", satellites)

            # Combina ambas mediciones en una lista antes de escribir en el archivo
            combined_measurements = [f" {level}", f" {latitude_d}", f" {latitude_m}", f" {longitude_d}", f" {longitude_m}", f" {altitude}", f" {satellites}"]
            
            with open(n_val + ".txt", 'a') as txt_file:
                txt_file.write(" ".join(combined_measurements))
                txt_file.write('\n')
            
            tb.stop()
            with open(n_val, 'w') as file:
                file.truncate(0)

            time.sleep(4)  # Espera 4 segundos antes de la próxima medición

        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GNU Radio script.')
    parser.add_argument('-d', '--distance', type=float, default=-5, help='Input for d value')
    parser.add_argument('-f', '--freq', type=float, default=0, help='Input for frequency value')
    parser.add_argument('-g', '--gain', type=float, default=20, help='Input for gain value')
    parser.add_argument('-n', '--name', type=str, default="medidas", help='Input for name value')
    args = parser.parse_args()
    main(d_val=args.distance, f_val=args.freq, g_val=args.gain, n_val=args.name)
