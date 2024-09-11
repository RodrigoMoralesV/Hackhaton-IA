import pandas as pd

# Ruta del archivo
path_file = 'csv/Dataset_vacunacion_clean.csv'

# Leer el CSV generado por el archivo convertirTXTaCSV.py'
df_vacunacion = pd.read_csv(path_file, sep='|')

# Verifcar el nombre de las columnas
c =  df_vacunacion.columns

## Obtener el numero de campos nulos
data_null = df_vacunacion.isnull()
data_nan = df_vacunacion.isna()

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

## Eliminar espacios en blanco al principio y final de los valores en las celdas
df_vacunacion = df_vacunacion.map(lambda x: x.strip() if isinstance(x, str) else x)

## Eliminar duplicados en base a la columna 'Documento', manteniendo la primera aparición
df_vacunacion = df_vacunacion.drop_duplicates(keep='first')

## Conocer la cantidad de personas sin grupo etnico
sin_grupo_etnico_count = df_vacunacion[df_vacunacion['GrupoEtnico'] == ""].shape[0]

## Sobreescribir los registros con "Ninguno de los anteriores". Donde "GrupoEtnico" es igual a ""
df_vacunacion.loc[df_vacunacion['GrupoEtnico'].str.strip() == '', 'GrupoEtnico'] = 'Ninguno de los anteriores'

# Crear un diccionario para mapear los valores
sex_map = {'Hombre': 1, 'Mujer': 2}

# Aplicar la transformación
df_vacunacion['Sexo'] = df_vacunacion['Sexo'].map(sex_map)

# 