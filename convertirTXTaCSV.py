"""
    LIMPIAR Y CONVERTIR .TXT A .CSV
"""

import csv

# ABRIR LA DATA Y LIMPARA PARA CONVERTIR A CSV
def eliminar_comillas_y_convertir_a_csv(archivo_txt, archivo_csv):
    # Abre el archivo en modo lectura
    with open(archivo_txt, 'r', encoding='utf-8') as file:
        # Lee el contenido del archivo
        contenido = file.read()

    # Reemplaza todas las comillas dobles y simples por una cadena vacía
    contenido_modificado = contenido.replace('"', '').replace("'", '')

    # Guardar el contenido modificado en el archivo original
    with open(archivo_txt, 'w', encoding='utf-8') as file:
        file.write(contenido_modificado)

    print(f"Las comillas dobles y simples han sido eliminadas del archivo {archivo_txt}.")

    # Convertir el archivo modificado a .csv sin añadir comillas
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as file_csv:
        writer = csv.writer(file_csv, quoting=csv.QUOTE_NONE, escapechar='\\')

        # Dividir el contenido en líneas
        lineas = contenido_modificado.splitlines()

        # Escribir cada línea como una fila en el archivo .csv
        for linea in lineas:
            writer.writerow([linea])

    print(f"El archivo ha sido convertido a {archivo_csv} sin añadir comillas.")

# Llamar a la función pasando el nombre del archivo .txt y el nombre del archivo .csv
eliminar_comillas_y_convertir_a_csv('data/Dataset_vacunacion.txt', 'csv/Dataset_vacunacion_clean.csv')