import csv
import pandas as pd
import unicodedata

# Función para convertir archivo de texto a CSV
def convert_txt_to_csv(txt_file, csv_file):
    with open(txt_file, 'r') as file:
        content = file.read()
        
    # Separar el contenido por el carácter '|' para obtener las filas
    rows = content.split('\n')
    
    # Extraer los encabezados de la primera fila
    headers = rows[0].split('|')
    
    # Crear el archivo CSV y escribir los datos
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for row in rows[1:]:
            values = row.split('|')
            writer.writerow(values)

    print(f"Archivo CSV generado: {csv_file}")


# Ejemplo de uso
convert_txt_to_csv('data/data_test.txt', 'csv/data_vacunacion.csv')

# Ruta del archivo
path_file = 'csv/data_vacunacion.csv'

# Leer el CSV generado
df_vacunacion = pd.read_csv(path_file, sep=',')

# LIMPIEZA DE DATOS

## Obtener el numero de campos nulos
data_null = df_vacunacion.isnull()
data_nan = df_vacunacion.isna()

## Eliminar los campos NaN
df_vacunacion = df_vacunacion.dropna()

## Eliminar comillas dobles al los extremos del texto
df_vacunacion = df_vacunacion.map(lambda x: str(x).replace('"', ''))
df_vacunacion.columns = [col.strip('"') for col in df_vacunacion.columns]

## Eliminar columnas sobrantes
df_vacunacion = df_vacunacion.drop(columns=[
    'TipoIdentificacion', 'direccionResidencia', 'CodMunicipioNacimiento', 'NombreMunicipioNacimiento',
    'CodDptoNacimiento',
    'NombreDptoNacimiento',
    'CodMunicipioResidencia',
    'NombreMunicipioResidencia',
    'CodDptoResidencia',
    'NombreDptoResidencia',
    'Desplazado',
    'Discapacitado',
    'RegimenAfiliacion',
    'CodigoAseguradora',
    'NombreAseguradora',
    'Codigo_Entidad',
    'estado"""	IdPaciente	Documento	PrimerNombre	PrimerApellido	direccionResidencia'
])

## Elimnar duplicados
data_duplicate = df_vacunacion.duplicated(subset=['Documento'], keep='first').sum()
duplicated_rows = df_vacunacion[df_vacunacion.duplicated(keep=False)]
duplicated_count = duplicated_rows.groupby(duplicated_rows.columns.tolist()).size().reset_index(name='counts')

## Eliminar espacios en blanco al principio y final de los nombres de columnas
df_vacunacion.columns = df_vacunacion.columns.str.strip()

df_vacunacion_apellidos = df_vacunacion['PrimerApellido']

## Eliminar espacios en blanco al principio y final de los valores en las celdas
df_vacunacion = df_vacunacion.map(lambda x: x.strip() if isinstance(x, str) else x)

## Eliminar duplicados en base a la columna 'Documento', manteniendo la primera aparición
df_vacunacion = df_vacunacion.drop_duplicates(keep='first')

## Contar los registros donde "FechaNacimiento" es igual a ""
sin_fecha_nacimiento_count = df_vacunacion[df_vacunacion['FechaNacimiento'] == ""].shape[0]

## Generar un DataFrame con los registros donde "FechaNacimiento" es igual a ""
df_sin_fecha_nacimiento = df_vacunacion[df_vacunacion['FechaNacimiento'] == ""]

## Eliminar los registros donde "FechaNacimiento" es igual a ""
df_vacunacion = df_vacunacion[df_vacunacion['FechaNacimiento'] != ""]

## Conocer la cantidad de personas sin grupo etnico
sin_grupo_etnico_count = df_vacunacion[df_vacunacion['GrupoEtnico'] == ""].shape[0]

## Sobreescribir los registros con "Ninguno de los anteriores". Donde "GrupoEtnico" es igual a ""
df_vacunacion.loc[df_vacunacion['GrupoEtnico'].str.strip() == '', 'GrupoEtnico'] = 'Ninguno de los anteriores'

# Crear un diccionario para mapear los valores
sex_map = {'Hombre': 1, 'Mujer': 2}

# Aplicar la transformación
df_vacunacion['Sexo'] = df_vacunacion['Sexo'].map(sex_map)
