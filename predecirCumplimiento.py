# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 08:46:23 2024

@author: Rodrigo
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, roc_curve, auc
import numpy as np

# Cargar los datos
df = pd.read_csv('csv/data_mart_frecuencia_neumococo_13.csv', sep='|', encoding = 'latin1')

# Preprocesamiento
df['fechanacimiento'] = pd.to_datetime(df['fechanacimiento'])
df['fecha_limite'] = pd.to_datetime(df['fecha_limite'])

# Crear características basadas en fechas
df['edad_dias'] = (pd.Timestamp.now() - df['fechanacimiento']).dt.days
df['dias_hasta_limite'] = (df['fecha_limite'] - pd.Timestamp.now()).dt.days

# Crear variable objetivo (cumplimiento del esquema de vacunación)
df['esquema_completo'] = (df['total_vacunas'] / 3) >= 0.9

# Codificar variables categóricas
le = LabelEncoder()
df['tipoidentificacion'] = le.fit_transform(df['tipoidentificacion'])
df['nombremunicipioresidencia'] = le.fit_transform(df['nombremunicipioresidencia'])
df['discapacitado'] = le.fit_transform(df['discapacitado'])

# Seleccionar características relevantes
features = ['tipoidentificacion', 'edad_dias', 'dias_hasta_limite', 'nombremunicipioresidencia', 'discapacitado', 
            'frecuencia_vacunacion', 'frecuencia_nacimiento_primera', 'frecuencia_primera_segunda', 
            'frecuencia_segunda_tercera', 'frecuencia_general']

X = df[features]
y = df['esquema_completo']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy:.2f}")

# Predecir para el año 2026
future_data = X.copy()
future_data['edad_dias'] = (pd.Timestamp('2026-01-01') - df['fechanacimiento']).dt.days
future_data['dias_hasta_limite'] = (df['fecha_limite'] - pd.Timestamp('2026-01-01')).dt.days
future_predictions = model.predict(future_data)

compliance_rate_2026 = np.mean(future_predictions)
print(f"Tasa de cumplimiento predicha para 2026: {compliance_rate_2026:.2f}")

if compliance_rate_2026 >= 0.9:
    print("El modelo predice que se cumplirá el esquema de vacunación en un 90% o más para el año 2026.")
else:
    print("El modelo predice que NO se cumplirá el esquema de vacunación en un 90% para el año 2026.")
    
plt.figure(figsize=(10, 6))
feature_importance = pd.DataFrame({'feature': features, 'importance': model.feature_importances_})
feature_importance = feature_importance.sort_values('importance', ascending=False)
sns.barplot(x='importance', y='feature', data=feature_importance)
plt.title('Importancia de las características')
plt.tight_layout()
plt.savefig('importancia_caracteristicas.png')
plt.close()

#Distribución de predicciones para 2026
plt.figure(figsize=(10, 6))
sns.histplot(future_predictions, kde=True)
plt.axvline(x=0.9, color='r', linestyle='--', label='Objetivo 90%')
plt.title('Distribución de predicciones de cumplimiento para 2026')
plt.xlabel('Probabilidad de cumplimiento')
plt.ylabel('Frecuencia')
plt.legend()
plt.tight_layout()
plt.savefig('distribucion_predicciones_2026.png')
plt.close()

print("Los gráficos se han guardado como archivos PNG en el directorio actual.")