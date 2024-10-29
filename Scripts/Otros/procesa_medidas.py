import os
import glob
import argparse
import math
from math import pow

class Procesa_Medidas:

    def calcula_altitud(presion, presion_nivel_mar) -> float:
            """The altitude based on the sea level pressure (:attr:`sea_level_pressure`)
            - which you must enter ahead of time)"""
            p = presion # in Si units for hPascal
            return 44330 * (1.0 - math.pow(p / presion_nivel_mar, 0.1903))+30

    def procesar_archivo(input_path, output_path, presion_nivel_mar):
        with open(input_path, 'r') as input_file:
            lines = input_file.readlines()

        output_folder = os.path.join(output_path, os.path.basename(os.path.dirname(input_path)))
        os.makedirs(output_folder, exist_ok=True)

        output_txt_path = os.path.join(output_folder, os.path.basename(input_path))
        with open(output_txt_path, 'w') as output_txt_file:
            for line in lines:
                columns = line.split()
                output_txt_file.write(f"{columns[0]} {columns[4]}\n")
        
        output_kml_path = os.path.splitext(output_txt_path)[0] + '.kml'
                
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

        with open(output_kml_path, 'w') as kml_file:
            kml_file.write(kml_header + kml_body + kml_footer)

    def procesar_carpeta(input_folder, output_folder, presion_nivel_mar):
        archivos_txt = glob.glob(os.path.join(input_folder, '**/*.txt'), recursive=True)

        for archivo_txt in archivos_txt:
            procesar_archivo(archivo_txt, output_folder,presion_nivel_mar)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Potencia_Distancia script.')
    parser.add_argument('-in', '--input', type=str, default='/home/pelayo/Desktop/Medidas/8a_prueba', help='Input directory')
    parser.add_argument('-out', '--output', type=str, default='/home/pelayo/Desktop/Resultados/7a_prueba', help='Output directory')
    parser.add_argument('-pr', '--pressure', type=float, default=1017.3,  help='Input for pressure value')
    args = parser.parse_args()
    Procesa_Medidas.procesar_carpeta(args.input, args.output, args.pressure)
