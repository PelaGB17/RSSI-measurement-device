from geopy.distance import geodesic
import  tkinter as tk
import tkinter.filedialog
import os
import math
import csv

def calcular_altura(presion, presion_nivel_mar) -> float:
    p = presion # in Si units for hPascal
    if presion == None:
        return None
    return 44330 * (1.0 - math.pow(p / presion_nivel_mar, 0.1903))+30

def calcular_distancia(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).meters

def actualizar_medidas(ruta):
    presion_nivel_mar = input("Introduce la presión a nivel del mar (hPa): ")
    if presion_nivel_mar != "":
        do_altura = True
        presion_nivel_mar = float(presion_nivel_mar)

    lat_transmisor = input("Introduce la latitud del transmisor: ")
    if lat_transmisor != "":
        do_distancia = True
        lat_transmisor = float(lat_transmisor)
    lon_transmisor = input("Introduce la longitud del transmisor: ")
    if lon_transmisor != "":
        do_distancia = True
        lon_transmisor = float(lon_transmisor)

    # Construir la ruta del archivo medidas.txt
    ruta_datos = os.path.join("Medidas", ruta, "medidas.txt")

    with open(ruta_datos, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        rows = list(reader)

    for row in rows:
        if len(row) < 8:
            continue  # Si la fila no tiene al menos 8 columnas, la ignoramos
        try:
            lat_receptor = float(row[1])
            lon_receptor = float(row[2])
            presion_atm = float(row[3])

            if do_altura:
                altura = calcular_altura(presion_nivel_mar, presion_atm)
            if do_distancia:
                distancia = calcular_distancia(lat_transmisor, lon_transmisor, lat_receptor, lon_receptor)

            row[4] = f"{distancia:.2f}"  # Actualizar distancia en la columna 5
            row[5] = f"{altura:.2f}"    # Actualizar altura en la columna 6
        except ValueError:
            continue  # Ignorar filas con datos no numéricos

    with open(ruta_datos, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerows(rows)



if __name__ == "__main__":
    ruta = tk.filedialog.askdirectory()
    actualizar_medidas(ruta)
