import argparse
from geopy.distance import great_circle

def calcular_distancia(lat1, lon1, lat2, lon2):
    punto1 = (lat1, lon1)
    punto2 = (lat2, lon2)
    distancia_km = great_circle(punto1, punto2).kilometers
    distancia_metros = distancia_km * 1000
    return distancia_metros

def generar_archivo_con_distancias(archivo_entrada, latitud, longitud, archivo_salida):
    with open(archivo_entrada, 'r') as f_entrada, open(archivo_salida, 'w') as f_salida:
        for linea in f_entrada:
            datos = linea.strip().split()
            lat = float(datos[1])
            lon = float(datos[2])
            distancia = calcular_distancia(lat, lon, latitud, longitud)
            f_salida.write(f"{datos[0]}\t{distancia:.2f}\n")

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Calcular distancias entre puntos en un archivo y un punto dado")
    parser.add_argument('-in', '--input', default='/home/pelayo/Desktop/Medidas/10a_prueba/medidas.txt' , help="Ruta del archivo de entrada")
    parser.add_argument('-lat', '--latitude', type=float, default=43.52462320, help="Latitud del punto dado")
    parser.add_argument('-lon', '--longitude', type=float, default=-5.63529600, help="Longitud del punto dado")
    parser.add_argument('-out', '--output', default='/home/pelayo/Desktop/Medidas/10a_prueba/procesado2.txt', help="Nombre del archivo de salida")
    args = parser.parse_args()

    generar_archivo_con_distancias(args.input, args.latitude, args.longitude, args.output)
