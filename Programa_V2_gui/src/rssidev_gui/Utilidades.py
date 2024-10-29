from geopy.distance import geodesic
import os
import math
import numpy

def obtener_distancia_gps(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).meters

def calcula_altitud(presion, presion_nivel_mar) -> float:
            p = presion # in Si units for hPascal
            if presion == None:
                return None
            return 44330 * (1.0 - math.pow(p / presion_nivel_mar, 0.1903))+30

def obtener_medidas(n_val):
    # Obtiene las mediciones de GNURadio del archivo binario
    with open(n_val, 'rb') as bin_file:
        f = numpy.fromfile(bin_file, dtype=numpy.float32)
            
    # Formatea la medicion de GNURadio
    for i in range(0, len(f), 2):
        level=str(f[i])
    
    #Borra la línea del archivo binario
    with open(n_val, 'w') as file:
        file.truncate(0)

    return level

def crear_siguiente_carpeta(directorio_base, nombre_base):
    subcarpetas = [nombre for nombre in os.listdir(directorio_base) if os.path.isdir(os.path.join(directorio_base, nombre))]

    numeros = [int(nombre.split('a')[0]) for nombre in subcarpetas]
    if numeros:
        siguiente_numero = max(numeros) + 1
    else:
        siguiente_numero = 1

    nuevo_nombre = f"{siguiente_numero}{nombre_base}"
    
    nueva_ruta = os.path.join(directorio_base, nuevo_nombre)
    os.mkdir(nueva_ruta)

    return nueva_ruta

def procesar_archivo(path, n_val):
        with open(path+ "/" + n_val + ".txt", 'r') as input_file:
            lines = input_file.readlines()

        with open(path+ "/" + "procesado" + ".txt", 'w') as output_txt_file:
            for line in lines:
                columns = line.split()
                output_txt_file.write(f"{columns[8]} {columns[4]} {columns[7]}\n")
                
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
            kml_body += kml_placemark_template.format(name=name, measure=data[0], longitude=data[2], latitude=data[1], altitude=data[6])

        with open(path+ "/" + "procesado" + ".kml", 'w') as kml_file:
            kml_file.write(kml_header + kml_body + kml_footer)
