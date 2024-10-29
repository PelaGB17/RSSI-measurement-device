import gpsd
import argparse
import time

def guardar_datos(latitud, longitud, altura, namefile):
    with open("/home/pelayo/Desktop/Prueba_GPS/" + namefile + ".txt", "a") as output_txt_file:
        output_txt_file.write(f"{latitud} {longitud} {altura}\n")
        
def procesar_archivo(namefile):
        with open("/home/pelayo/Desktop/Prueba_GPS/" + namefile + ".txt", 'r') as input_file:
            lines = input_file.readlines()
                
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
                          <Point>
                        </Placemark>
                    """
        kml_body = ""
            
        for i, line in enumerate(lines):
            data = line.split()
            name = f"Medida_{i + 1}"
            kml_body += kml_placemark_template.format(name=name, longitude=data[1], latitude=data[0], altitude=data[2])

        with open("/home/pelayo/Desktop/Prueba_GPS/" + "procesado_kml" + ".txt", 'w') as kml_file:
            kml_file.write(kml_header + kml_body + kml_footer)

def main(n_val="gps", options = None):
    
    gpsd.connect()
    iteracion = 1
    print("Recopilando datos de GPS. Presione Ctrl+C para detener.")
    try:
        while True:
            # Obtener los datos de posición
            paquete = gpsd.get_current()
            latitud = paquete.lat
            longitud = paquete.lon
            altura = paquete.alt
            print (iteracion)
            
            guardar_datos(latitud, longitud, altura, n_val)
            iteracion = iteracion + 1 
            
            time.sleep(1)

    except KeyboardInterrupt:
        procesar_archivo(n_val)
        pass
        
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, default="gps_2", help='Input for name value')
    args = parser.parse_args()
    main(n_val=args.name)
