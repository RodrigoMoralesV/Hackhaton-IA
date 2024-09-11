import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta

# Cargar los datos del CSV
df_vacunacion = pd.read_csv("csv/Dataset_vacunacion_clean.csv", sep='|')

# Verificar las columnas del DataFrame
print("Columnas en df_vacunacion:")
print(df_vacunacion.columns)
print("\nPrimeras filas de df_vacunacion:")
print(df_vacunacion.head())

# Preparar los datos
fecha_referencia = datetime(1900, 1, 1)
df_vacunacion['FechaNacimiento'] = pd.to_datetime(df_vacunacion['FechaNacimiento'], errors='coerce')
df_vacunacion['dias_desde_referencia'] = (df_vacunacion['FechaNacimiento'] - fecha_referencia).dt.days

le = LabelEncoder()
df_vacunacion['TipoIdentificacion_encoded'] = le.fit_transform(df_vacunacion['TipoIdentificacion'])

# Manejar valores nulos
df_completo = df_vacunacion.dropna(subset=['FechaNacimiento', 'TipoIdentificacion', 'Documento'])

# Dividir en conjunto de entrenamiento y prueba
X = df_completo[['TipoIdentificacion_encoded', 'Documento']]
y = df_completo['dias_desde_referencia']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"\nError absoluto medio: {mae:.2f} días")

# Función para predecir fecha de nacimiento
def predecir_fecha_nacimiento(tipo_documento, numero_documento):
    tipo_encoded = le.transform([tipo_documento])[0]
    dias_predichos = model.predict([[tipo_encoded, numero_documento]])
    return fecha_referencia + timedelta(days=int(dias_predichos[0]))

# Predecir fechas faltantes
df_vacunacion['FechaNacimiento_predicha'] = df_vacunacion.apply(
    lambda row: predecir_fecha_nacimiento(row['TipoIdentificacion'], row['Documento'])
    if pd.isnull(row['FechaNacimiento']) else row['FechaNacimiento'],
    axis=1
)

# Mostrar ejemplos de predicciones
print("\nEjemplos de predicciones:")
ejemplos = df_vacunacion[df_vacunacion['FechaNacimiento'].isnull()].head(5)
for _, row in ejemplos.iterrows():
    print(f"Tipo: {row['TipoIdentificacion']}, Número: {row['Documento']}")
    print(f"Fecha de nacimiento predicha: {row['FechaNacimiento_predicha'].strftime('%Y-%m-%d')}")
    print("---")

# Analizar importancia de características
importancia = model.feature_importances_
print("\nImportancia de características:")
print(f"Tipo de Documento: {importancia[0]:.4f}")
print(f"Número de Documento: {importancia[1]:.4f}")

# Estadísticas sobre datos faltantes
total_registros = len(df_vacunacion)
registros_con_fecha = df_vacunacion['FechaNacimiento'].notnull().sum()
registros_sin_fecha = df_vacunacion['FechaNacimiento'].isnull().sum()

print(f"\nTotal de registros: {total_registros}")
print(f"Registros con fecha de nacimiento: {registros_con_fecha}")
print(f"Registros sin fecha de nacimiento (predichos): {registros_sin_fecha}")
print(f"Porcentaje de registros predichos: {(registros_sin_fecha/total_registros)*100:.2f}%")

# Guardar el DataFrame actualizado
df_vacunacion.to_csv("csv/datos_vacunacion_actualizados.csv", index=False, sep='|')
print("\nDataFrame actualizado guardado en 'datos_vacunacion_actualizados.csv'")