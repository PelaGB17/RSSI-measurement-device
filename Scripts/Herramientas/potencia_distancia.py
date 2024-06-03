import os
import glob
from math import pow
from geopy.distance import geodesic
import argparse

        
def obtener_distancia_gps(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).meters

def procesar_archivo(input_path, output_path, lat, lon):
    with open(input_path, 'r') as input_file:
        lines = input_file.readlines()

    with open(output_path, 'w') as output_txt_file:
        for line in lines:
            columns = line.split()
            distancia= obtener_distancia_gps(columns[1], columns[2], lat, lon)
            output_txt_file.write(f"{columns[0]} {distancia}\n")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Potencia_Distancia script.')
    parser.add_argument('-lat', '--latitude', type=float, default=0, help='Input for latitude value')
    parser.add_argument('-lon', '--longitude', type=float, default=0, help='Input for longitude value')
    parser.add_argument('-in', '--input', type=str, default='/home/pelayo/Desktop/Resultados_original/6a_prueba/medidas.txt', help='Input directory')
    parser.add_argument('-out', '--output', type=str, default='/home/pelayo/Desktop/Resultados_original/6a_prueba/medida.txt', help='Output directory')
    parser.add_argument('-pr', '--pressure', type=float, default=0, help='Input for pressure value')
    args = parser.parse_args()
    procesar_archivo(args.input, args.output, args.latitude, args.longitude)
    
