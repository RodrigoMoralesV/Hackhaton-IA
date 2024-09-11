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

###### VECTORIZACION

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

data_file = 'csv/dataset_frag.csv'
df = pd.read_csv(data_file, sep = '|')

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df)

# Determinar el número óptimo de cluster usando el metodo del codo
sse = []
for k in range(2, 16):
    kmeans = KMeans(n_clusters = k, n_init = 10, random_state = 0).fit(X)
    sse.append(kmeans.inertia_)
    
# Convertir el rango de SEE a DataFrame para asegugar no tener valores
sse_df = pd.DataFrame({'clusters': range(2, 16), 'sse': sse})
sse_df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Graficar el método del codo
plt.figure(figsize=(8,5))
sns.lineplot(x='clusters', y='sse', data=sse_df, marker='o')
plt.title('Método del codo para encontrar el número óptimo de clusters')
plt.xlabel('Número de clustess')
plt.ylabel('SSE')
plt.show()

# Elegir el número óptimo de clusters
n_clusters = 15
kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=0).fit(X)
df['Patron'] = kmeans.labels_