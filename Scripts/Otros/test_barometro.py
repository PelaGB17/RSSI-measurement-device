import numpy as np
import matplotlib.pyplot as plt

# Leer y procesar el archivo
file_name = 'Barometro2.txt'

def leer_datos(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    periodos = []
    periodo_actual = []

    for line in lines:
        if "Cambio de escenario" in line:
            if periodo_actual:
                periodos.append(periodo_actual)
                periodo_actual = []
        else:
            # Extraer la altitud del texto
            partes = line.strip().split(',')
            for parte in partes:
                if "Altura" in parte:
                    altura = float(parte.split(':')[1].strip().split()[0])
                    periodo_actual.append(altura)
    
    if periodo_actual:
        periodos.append(periodo_actual)

    return periodos

def crear_subplots(periodos):
    num_periodos = len(periodos)
    titulos = ['Tapado', 'Destapado', 'Destapado con vibración', 'Tapado con vibración']
    fig, axes = plt.subplots(num_periodos, 1, figsize=(10, num_periodos * 4))

    if num_periodos == 1:
        axes = [axes]  # Asegurar que axes sea iterable si hay un solo subplot

    for i, periodo in enumerate(periodos):
        ax = axes[i]
        alturas = np.array(periodo)
        tiempo = np.arange(len(alturas))  # Asumiendo que cada medida es cada 30s

        # Calcular media y desviación estándar
        media = np.mean(alturas)
        std_dev = np.std(alturas)

        # Graficar las alturas
        ax.plot(tiempo, alturas, marker='o', linestyle='-')
        ax.set_title(titulos[i])
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Altura (m)')

        # Añadir cuadro de texto con estadísticas
        textstr = f'Media: {media:.2f} m\nDesviación típica: {std_dev:.2f} m'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.show()

# Leer datos y crear subplots
periodos = leer_datos(file_name)
crear_subplots(periodos)
