import os

def txt_to_kml(input_dir, output_dir):
    if not os.path.exists(input_dir):
        print(f"Error: El directorio de entrada '{input_dir}' no existe.")
        return

    for subdir, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                input_path = os.path.join(subdir, file)

                with open(input_path, 'r') as f:
                    lines = f.readlines()

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
                    measure, altitude, longitude, latitude = data[0], data[1], data[2], data[3]
                    name = f"Medida_{i + 1}"
                    kml_body += kml_placemark_template.format(name=name, measure=measure, longitude=longitude, latitude=latitude, altitude=altitude)

                output_subdir = os.path.relpath(subdir, input_dir)
                output_file = f"{os.path.splitext(file)[0]}.kml"
                output_path = os.path.join(output_dir, output_subdir, output_file)

                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'w') as kml_file:
                    kml_file.write(kml_header + kml_body + kml_footer)

if __name__ == "__main__":
    input_directory = "/home/pelayo/Desktop/Medidas"  # Ruta a la carpeta que contiene los subdirectorios con archivos .txt
    output_directory = "/home/pelayo/Desktop/Resultados"  # Ruta a la carpeta de salida

    txt_to_kml(input_directory, output_directory)
