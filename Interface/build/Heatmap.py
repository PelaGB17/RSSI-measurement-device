import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pyproj import Proj, Transformer
from scipy.interpolate import griddata

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
    transformer = Transformer.from_crs("epsg:4326", proyecto_utm.crs)
    
    # Convertir las coordenadas a metros
    x, y = transformer.transform(latitud, longitud)
    return x, y

# Función para crear los subplots del mapa de calor y el perfil de elevación
def crear_subplots(datos, ruta_guardado):
    # Convertir latitud y longitud a metros
    datos['x'], datos['y'] = convertir_a_metros(datos[1].values, datos[2].values)
    
    # Crear una malla de puntos regular para la interpolación
    x_grid = np.linspace(datos['x'].min(), datos['x'].max(), 100)
    y_grid = np.linspace(datos['y'].min(), datos['y'].max(), 100)
    X, Y = np.meshgrid(x_grid, y_grid)
    
    # Interpolar los valores de nivel de señal y altura en la malla
    Z_signal = griddata((datos['x'], datos['y']), datos[0], (X, Y), method='linear')
    Z_height = griddata((datos['x'], datos['y']), datos[5], (X, Y), method='linear')
    
    # Crear los subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    
    # Subplot para el mapa de calor del nivel de señal
    ax1 = axes[0]
    im1 = ax1.imshow(Z_signal, extent=(x_grid.min(), x_grid.max(), y_grid.min(), y_grid.max()), origin='lower', cmap='viridis')
    ax1.plot(datos['x'], datos['y'], color='red', linestyle='-', linewidth=2, markersize=4, marker='x', label='Trayectoria')
    ax1.set_title('Mapa de calor del nivel de señal')
    ax1.set_xlabel('Metros')
    ax1.set_ylabel('Metros')
    ax1.legend()
    fig.colorbar(im1, ax=ax1, label='Nivel de señal')
    
    # Subplot para el perfil de elevación del terreno
    ax2 = axes[1]
    im2 = ax2.imshow(Z_height, extent=(x_grid.min(), x_grid.max(), y_grid.min(), y_grid.max()), origin='lower', cmap='terrain')
    ax2.plot(datos['x'], datos['y'], color='red', linestyle='-', linewidth=2, markersize=4, marker='x', label='Trayectoria')
    ax2.set_title('Perfil de elevación del terreno')
    ax2.set_xlabel('Metros')
    ax2.set_ylabel('Metros')
    ax2.legend()
    fig.colorbar(im2, ax=ax2, label='Altura')
    
    # Guardar la figura como archivo PNG
    plt.tight_layout()
    plt.savefig(ruta_guardado)
    plt.show()

# Función principal
def main(prueba):
    # Solicitar al usuario el nombre de la prueba
    prueba += "a_Prueba"

    # Construir la ruta del archivo medidas.txt
    ruta_datos = os.path.join("Medidas", prueba, "medidas.txt")
    
    # Ruta donde se guardará el archivo PNG
    archivo = prueba + ".png"
    ruta_guardado = os.path.join("Medidas", prueba, archivo)

    # Cargar los datos
    datos = cargar_datos(ruta_datos)

    if datos is not None:
        # Eliminar filas con NaN (si las hay)
        datos = datos.dropna()

        # Crear y guardar los subplots
        crear_subplots(datos, ruta_guardado)