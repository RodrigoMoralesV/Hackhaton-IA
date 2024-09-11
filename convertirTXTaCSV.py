"""
    LIMPIAR Y CONVERTIR .TXT A .CSV
"""
import csv

def eliminar_comillas_y_convertir_a_csv(archivo_txt, archivo_csv):
    # Abre el archivo en modo lectura
    with open(archivo_txt, 'r', encoding='latin1') as file:
        # Lee el contenido del archivo
        contenido = file.read()
    
    # Reemplaza todas las comillas dobles y simples por una cadena vacía
    contenido_modificado = contenido.replace('"', '').replace("'", '')
    
    # Guardar el contenido modificado en el archivo original
    with open(archivo_txt, 'w', encoding='latin1') as file:
        file.write(contenido_modificado)
    print(f"Las comillas dobles y simples han sido eliminadas del archivo {archivo_txt}.")
    
    # Convertir el archivo modificado a .csv sin añadir comillas
    with open(archivo_csv, 'w', newline='', encoding='latin1') as file_csv:
        writer = csv.writer(file_csv, quoting=csv.QUOTE_NONE, escapechar='\\')
        
        # Dividir el contenido en líneas
        lineas = contenido_modificado.splitlines()
        
        # Escribir la cabecera
        if lineas:
            writer.writerow([lineas[0]])
        
        # Escribir los registros, saltando una línea después de cada uno
        for i in range(1, len(lineas), 2):
            if i < len(lineas):
                writer.writerow([lineas[i]])
    
    print(f"El archivo ha sido convertido a {archivo_csv} sin añadir comillas y eliminando líneas después de la cabecera y cada registro.")

# Llamar a la función pasando el nombre del archivo .txt y el nombre del archivo .csv
eliminar_comillas_y_convertir_a_csv('data/Dataset_vacunacion.txt', 'csv/Dataset_vacunacion_clean.csv')
