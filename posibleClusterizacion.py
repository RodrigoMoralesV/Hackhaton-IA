import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy import stats

# Cargar y preparar los datos
df_fre = pd.read_csv("csv/data_mart_frecuencia_neumococo_13.csv", sep='|', encoding='latin1')
df_fre['frecuencia_general'].fillna(0, inplace=True)

# Normalizar la columna frecuencia_general
scaler = StandardScaler()
df_fre['frecuencia_general_scaled'] = scaler.fit_transform(df_fre[['frecuencia_general']])

# Aplicar K-Means con diferentes números de clusters (1 a 15)
inertia = []
for k in range(1, 16):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_fre[['frecuencia_general_scaled']])
    inertia.append(kmeans.inertia_)

# Visualizar el método del codo
plt.figure(figsize=(10, 6))
plt.plot(range(1, 16), inertia, marker='o', linestyle='--')
plt.title('Método del Codo para K-Means')
plt.xlabel('Número de Clusters')
plt.ylabel('Inercia')
plt.show()

# Aplicar K-Means con el número óptimo de clusters
k_optimo = 3  # Ajustar este valor según el gráfico del codo
kmeans_opt = KMeans(n_clusters=k_optimo, random_state=42)
df_fre['cluster'] = kmeans_opt.fit_predict(df_fre[['frecuencia_general_scaled']])

print("Primeras filas del DataFrame con clusters asignados:")
print(df_fre[['tipoidentificacion', 'frecuencia_general', 'cluster']].head())

# Análisis post-clusterización

# 1. Perfilado de clusters
cluster_profiles = df_fre.groupby('cluster').agg({
    'frecuencia_general': ['mean', 'std', 'min', 'max']
})
print("\nPerfiles de Clusters:")
print(cluster_profiles)

# 2. Visualización avanzada: Gráfico de violín
plt.figure(figsize=(12, 6))
sns.violinplot(x='cluster', y='frecuencia_general', data=df_fre)
plt.title('Distribución de Frecuencia General por Cluster')
plt.show()

# 3. Análisis de outliers
# Llenar los valores nulos en la columna 'frecuencia_general'
df_fre['frecuencia_general'].fillna(0, inplace=True)

# Análisis de outliers usando z-scores
z_scores = np.abs(stats.zscore(df_fre[['frecuencia_general']]))
outliers = df_fre[(z_scores > 3).any(axis=1)]

# Mostrar los outliers detectados
outliers_detected = outliers[['tipoidentificacion', 'frecuencia_general']]
outliers_detected.head()

# Diagrama de outliers
plt.figure(figsize=(10, 6))
plt.boxplot(df_fre['frecuencia_general'])
plt.title('Diagrama de Outliers para Frecuencia General')
plt.ylabel('Frecuencia General')
plt.show()

# 4. Análisis de tendencias temporales (simulado)
# Agregamos una columna de fecha simulada para este ejemplo
end_date = datetime.now()
df_fre['Fecha'] = [end_date - timedelta(days=i) for i in range(len(df_fre))]

# Verificar el tipo de datos de la columna 'Fecha'
print("Tipo de datos de la columna 'Fecha':", df_fre['Fecha'].dtype)

# Convertir la columna 'Fecha' a datetime
# Si la columna 'Fecha' es de tipo objeto (string), usamos pd.to_datetime
if df_fre['Fecha'].dtype == 'object':
    df_fre['Fecha'] = pd.to_datetime(df_fre['Fecha'], errors='coerce')
# Si la columna 'Fecha' es de tipo numérico (timestamp), usamos pd.to_datetime con unit='s'
elif df_fre['Fecha'].dtype in ['int64', 'float64']:
    df_fre['Fecha'] = pd.to_datetime(df_fre['Fecha'], unit='s')

df_fre['Mes'] = df_fre['Fecha'].dt.to_period('M')

trend_analysis = df_fre.groupby(['Mes', 'cluster'])['frecuencia_general'].mean().reset_index()

plt.figure(figsize=(12, 6))
for cluster in df_fre['cluster'].unique():
    cluster_data = trend_analysis[trend_analysis['cluster'] == cluster]
    plt.plot(cluster_data['Mes'].astype(str), cluster_data['frecuencia_general'], label=f'Cluster {cluster}')

plt.title('Tendencia de Frecuencia General por Cluster a lo largo del tiempo')
plt.xlabel('Mes')
plt.ylabel('Frecuencia General Media')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Recomendaciones basadas en clusters
def get_recommendations(cluster):
    if cluster == 0:
        return "Aumentar la promoción de la vacunación"
    elif cluster == 1:
        return "Mantener la estrategia actual"
    else:
        return "Investigar factores que influyen en la alta frecuencia"

df_fre['Recomendacion'] = df_fre['cluster'].apply(get_recommendations)
print("\nEjemplo de recomendaciones:")
print(df_fre[['tipoidentificacion', 'cluster', 'Recomendacion']].head(10))

# 6. Distribución de tipos de identificación por cluster
id_type_distribution = df_fre.groupby(['cluster', 'tipoidentificacion']).size().unstack(fill_value=0)
id_type_distribution_percentage = id_type_distribution.div(id_type_distribution.sum(axis=1), axis=0) * 100

plt.figure(figsize=(12, 6))
id_type_distribution_percentage.plot(kind='bar', stacked=True)
plt.title('Distribución de Tipos de Identificación por Cluster')
plt.xlabel('Cluster')
plt.ylabel('Porcentaje')
plt.legend(title='Tipo de Identificación', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

print("\nDistribución de Tipos de Identificación por Cluster (%):")
print(id_type_distribution_percentage)