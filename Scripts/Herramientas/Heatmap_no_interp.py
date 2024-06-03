import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyproj import Proj, transform

# Función para cargar los datos de medidas.txt
def cargar_datos(ruta):
    try:
        # Lee el archivo medidas.txt como un DataFrame de pandas
        df = pd.read_csv(ruta, sep='\s+', header=None)
        return df
    except FileNotFoundError:
        print("El archivo no existe en la ruta proporcionada.")
        return None

# Función para convertir latitud y longitud a metros
def convertir_a_metros(latitud, longitud):
    # Definir la proyección UTM
    proyecto_utm = Proj(proj='utm', zone=30, ellps='WGS84', units='m')
    
    # Convertir las coordenadas a metros
    x, y = transform(Proj("EPSG:4326"), proyecto_utm, longitud, latitud)
    return x, y

# Función para crear el mapa de calor del nivel de señal
def mapa_calor_nivel_de_senal(datos):
    # Convertir latitud y longitud a metros
    datos['x'], datos['y'] = convertir_a_metros(datos[1], datos[2])
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=datos, x='x', y='y', hue=0, palette='viridis', legend='full')
    plt.title('Mapa de calor del nivel de señal')
    plt.xlabel('Metros')
    plt.ylabel('Metros')
    # plt.colorbar(label='Nivel de señal')
    plt.show()

# Función para crear el perfil de elevación del terreno
def perfil_elevacion(datos):
    # Convertir latitud y longitud a metros
    datos['x'], datos['y'] = convertir_a_metros(datos[1], datos[2])
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=datos, x='x', y='y', hue=5, palette='terrain', legend='full')
    plt.title('Perfil de elevación del terreno')
    plt.xlabel('Metros')
    plt.ylabel('Metros')
    # plt.colorbar(label='Altura')
    plt.show()

# Función principal
def main():
    # Solicitar al usuario el nombre de la prueba
    prueba = input("Ingrese el nombre de la prueba (1a_Prueba, 2a_Prueba, etc.): ")
    prueba += "a_Prueba"

    # Construir la ruta del archivo medidas.txt
    ruta = os.path.join("Medidas", prueba, "medidas.txt")

    # Cargar los datos
    datos = cargar_datos(ruta)

    if datos is not None:
        # Eliminar filas con NaN (si las hay)
        datos = datos.dropna()

        # Crear mapa de calor del nivel de señal
        mapa_calor_nivel_de_senal(datos)

        # Crear perfil de elevación del terreno
        perfil_elevacion(datos)

if __name__ == "__main__":
    main()
