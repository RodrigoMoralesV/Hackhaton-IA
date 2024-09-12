from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df_fre = pd.read_csv("csv/data_mart_frecuencia_vacunacion.csv", sep = '|', encoding='latin1')

# Aseguramos que no haya valores NaN en la columna frecuencia_vacunacion
df_fre['frecuencia_vacunacion'].fillna(0, inplace=True)

# Paso 1: Normalizamos la columna frecuencia_vacunacion
scaler = StandardScaler()
df_fre['frecuencia_vacunacion_scaled'] = scaler.fit_transform(df_fre[['frecuencia_vacunacion']])

# Paso 2: Aplicamos K-Means con diferentes números de clusters (2 a 15)
inertia = []  # Lista para guardar la inercia (suma de distancias al centroide) para cada cluster

for k in range(1, 16):  # De 2 a 15 clusters
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_fre[['frecuencia_vacunacion_scaled']])
    inertia.append(kmeans.inertia_)

# Paso 3: Método del codo para encontrar el número óptimo de clusters
plt.figure(figsize=(8, 5))
plt.plot(range(1, 16), inertia, marker='o', linestyle='--')
plt.title('Método del Codo')
plt.xlabel('Número de Clusters')
plt.ylabel('Inercia')
plt.show()

# Paso 4: Asignamos el número óptimo de clusters (suponiendo que elegimos 4 clusters, ajustar según codo)
k_optimo = 4  # Ajustar este valor según el gráfico del codo
kmeans_opt = KMeans(n_clusters=k_optimo, random_state=42)
df_fre['cluster'] = kmeans_opt.fit_predict(df_fre[['frecuencia_vacunacion_scaled']])

# Paso 5: Verificamos los resultados
print(df_fre[['tipoidentificacion', 'frecuencia_vacunacion', 'cluster']].head())
