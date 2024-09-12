import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta

# Cargar los datos del CSV
df_vacunacion = pd.read_csv("csv/Dataset_vacunacion_normalizada.csv", sep='|', index_col=False, encoding='latin1')

# Verificar las columnas del DataFrame
print("Columnas en df_vacunacion:")
print(df_vacunacion.columns)
print("\nPrimeras filas de df_vacunacion:")
print(df_vacunacion.head())

# Convertir la columna 'FechaNacimiento' al formato deseado (solo fecha, sin hora)
df_vacunacion['FechaNacimiento'] = pd.to_datetime(df_vacunacion['FechaNacimiento'], errors='coerce').dt.date

# Continuar con la conversión de 'dias_desde_referencia'
fecha_referencia = datetime(1900, 1, 1)
df_vacunacion['dias_desde_referencia'] = (pd.to_datetime(df_vacunacion['FechaNacimiento']) - fecha_referencia).dt.days

# Preparar los datos
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

# Predecir fechas faltantes y guardarlas en la columna 'FechaNacimiento_predicha'
df_vacunacion['FechaNacimiento_predicha'] = df_vacunacion.apply(
    lambda row: predecir_fecha_nacimiento(row['TipoIdentificacion'], row['Documento'])
    if pd.isnull(row['FechaNacimiento']) else row['FechaNacimiento'],
    axis=1
)

# Reemplazar los valores NaN en 'FechaNacimiento' con los de 'FechaNacimiento_predicha'
df_vacunacion['FechaNacimiento'] = df_vacunacion['FechaNacimiento'].fillna(df_vacunacion['FechaNacimiento_predicha'])

# Asegurarse de que las fechas tengan el formato AAAA-MM-DD
df_vacunacion['FechaNacimiento'] = pd.to_datetime(df_vacunacion['FechaNacimiento']).dt.strftime('%Y-%m-%d')

# Mostrar ejemplos de las fechas actualizadas
print("\nEjemplos de registros con fechas actualizadas:")
ejemplos = df_vacunacion[df_vacunacion['FechaNacimiento_predicha'].notnull()].head(5)
for _, row in ejemplos.iterrows():
    print(f"Tipo: {row['TipoIdentificacion']}, Número: {row['Documento']}")
    print(f"Fecha de nacimiento actualizada: {row['FechaNacimiento']}")
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

print(df_vacunacion.index)

# Guardar el DataFrame actualizado
df_vacunacion.to_csv("csv/datos_vacunacion_actualizados.csv", index=False, sep='|')
print("\nDataFrame actualizado guardado en 'datos_vacunacion_actualizados.csv'")

df_actualizado = pd.read_csv("csv/datos_vacunacion_actualizados.csv", sep = '|')
