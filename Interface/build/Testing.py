import argparse
import sys
import time
import os
import signal
from GNU_Radio import GNURadioBlock
from GPS import inicializar_gps, obtener_datos_gps
from Barometro import inicializar_barometro, obtener_datos_barometro
from Pantalla import inicializar_pantalla, mostrar_datos_pantalla
from Utilidades import obtener_distancia_gps, calcula_altitud, obtener_medidas, procesar_archivo, crear_siguiente_carpeta

class main():
	print("Probando Barómetro...")
	time.sleep(1)
	barometro = inicializar_barometro()
	if (barometro != None):
		print("Inicialización correcta")
		a = obtener_datos_barometro(barometro)
		if (a != None):
			print("Datos obtenidos correctamente: " +  str(a))
	else:
		print("El GPS no está funcionando correctamente")
		sys.exit(0)	
	time.sleep(1)
	
	print("Probando GPS...")
	time.sleep(1)
	b = inicializar_gps()
	if (b != None):
		print("Inicialización de gps correcta")
		c = obtener_datos_gps()
		while  (c["altitude"] == None):
			print(".", end='')
			c = obtener_datos_gps()
			time.sleep(1)
		print("Datos obtenidos correctamente [altura]: " + str(c["altitude"]))
	else:
		print("El GPS no está funcionando correctamente")
		sys.exit(0)
	
	time.sleep(1)
		
	print("Probando Pantalla...")
	time.sleep(1)
	correct = False
	while (correct == False):
		pantalla = inicializar_pantalla()
		if (pantalla != None):
			print("Inicialización correcta")
			mostrar_datos_pantalla(pantalla, c)
			answer = input("¿Se muestran los datos correctamente? [s/N]: ")
			if answer == "s" or answer == "S":
				correct = True
				
	print("Todos los componentes funcionan correctamente")
	
if __name__ == '__main__':
	m = main()
