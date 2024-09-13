import pandas as pd
import numpy as np
import psycopg2

dbname = 'db_vacunacion'
user = "postgres"
password = "1234"
host = "localhost"
port = "5432"

data= {}

try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    print('Conexión exitosa')
    
    query = """
        select 
            tipoidentificacion,
            fechanacimiento, 
            nombremunicipioresidencia,
            discapacitado,
            neumococo_conjugado_10_valente_primera,
            neumococo_conjugado_10_valente_segunda,
            neumococo_conjugado_10_valente_refuerzo
        from 
            data_lake_fecha_predicha
    """
            
    data = pd.read_sql_query(query, conn)
    
except Exception as e:
    print(f"Error al conectarse a la base de datos: {e}")
    
finally:
    conn.close()
    
# Obtener las columnas son necesarias
df_fre = data

# Declarar las vacunas a analizar
columnas_vacunas = [
    'neumococo_conjugado_10_valente_primera',
    'neumococo_conjugado_10_valente_segunda',
    'neumococo_conjugado_10_valente_refuerzo'
    ]

###############################################################################################
#                       Calcular numero de vacunas desde 0 a 5 años                           #
###############################################################################################

# Aseguramos que las fechas sean tipo datetime
df_fre.loc[:, 'fechanacimiento'] = pd.to_datetime(data['fechanacimiento'], errors='coerce')

# Convertimos las columnas de vacunas a tipo datetime
df_fre[columnas_vacunas] = df_fre[columnas_vacunas].apply(pd.to_datetime, errors='coerce')

# Calculamos la fecha límite de los 5 años desde la fecha de nacimiento
df_fre.loc[:, 'fecha_limite'] = df_fre['fechanacimiento'] + pd.DateOffset(years=5)

# Función para contar las vacunas aplicadas antes de los 5 años
def contar_vacunas(row):
    count = 0
    for col in columnas_vacunas:
        # Verificamos si la fecha de la vacuna no es NaN y es anterior a la fecha límite
        if pd.notna(row[col]) and row[col] <= row['fecha_limite']:
            count += 1
    return count

# LLamado de la funcion para calcular
df_fre['vacunas_0_a_5'] = df_fre.apply(contar_vacunas, axis=1)


###############################################################################################
#                           Calcular la frecuencia de vacunación                              #
###############################################################################################

# Paso 1: Contar el número total de vacunas administradas (no NaN)
df_fre['total_vacunas'] = df_fre[columnas_vacunas].notna().sum(axis=1)

# Paso 2: Encontrar la fecha de la primera y la última vacuna aplicada
df_fre['primera_vacuna'] = df_fre[columnas_vacunas].min(axis=1)
df_fre['ultima_vacuna'] = df_fre[columnas_vacunas].max(axis=1)

# Paso 3: Calcular la diferencia de tiempo en días entre la primera y la última vacuna
df_fre['dias_entre_vacunas'] = (df_fre['ultima_vacuna'] - df_fre['primera_vacuna']).dt.days

# Paso 4: Calcular la frecuencia de vacunación (vacunas por día)
# Evitamos división por cero cuando no hay días entre la primera y la última vacuna
df_fre['frecuencia_vacunacion'] = df_fre['total_vacunas'] / df_fre['dias_entre_vacunas'].replace(0, np.nan)

# Verificamos los resultados
print(df_fre[['tipoidentificacion', 'total_vacunas', 'dias_entre_vacunas', 'frecuencia_vacunacion']].head())


###############################################################################################
#                             Calcular frecuencia entre distintas fechas                      #
###############################################################################################

# Aseguramos que las columnas sean tipo datetime (esto incluye manejar NaT)
df_fre['fechanacimiento'] = pd.to_datetime(df_fre['fechanacimiento'], errors='coerce')
df_fre[columnas_vacunas] = df_fre[columnas_vacunas].apply(pd.to_datetime, errors='coerce')

# Función para calcular la frecuencia de vacunación
def calcular_frecuencia(fecha_inicio, fecha_fin):
    dias = (fecha_fin - fecha_inicio).dt.days
    return np.where(dias > 0, 1 / dias, np.nan)

# Calcular frecuencias
df_fre['frecuencia_nacimiento_primera'] = calcular_frecuencia(
    df_fre['fechanacimiento'], 
    df_fre['neumococo_conjugado_10_valente_primera']
)

df_fre['frecuencia_primera_segunda'] = calcular_frecuencia(
    df_fre['neumococo_conjugado_10_valente_primera'], 
    df_fre['neumococo_conjugado_10_valente_segunda']
)

df_fre['frecuencia_segunda_refuerzo'] = calcular_frecuencia(
    df_fre['neumococo_conjugado_10_valente_segunda'], 
    df_fre['neumococo_conjugado_10_valente_refuerzo']
)

###############################################################################################
#                 Calcular la frecuencia general del esquema de vacunación                    #
###############################################################################################
def calcular_frecuencia_general(row):
    frecuencias = [row['frecuencia_nacimiento_primera'], 
                   row['frecuencia_primera_segunda'], 
                   row['frecuencia_segunda_refuerzo']]
    frecuencias_validas = [f for f in frecuencias if pd.notna(f)]
    
    if len(frecuencias_validas) > 0:
        # Calculamos un promedio ponderado
        # La primera frecuencia tiene peso 1, la segunda peso 2, y la tercera peso 3
        pesos = list(range(1, len(frecuencias_validas) + 1))
        return np.average(frecuencias_validas, weights=pesos)
    else:
        return np.nan

df_fre['frecuencia_general'] = df_fre.apply(calcular_frecuencia_general, axis=1)

# Verificamos los resultados
print(df_fre[['tipoidentificacion', 'frecuencia_nacimiento_primera', 'frecuencia_primera_segunda', 
              'frecuencia_segunda_refuerzo', 'frecuencia_general']].head())


###############################################################################################
#                        Generar CSV SOLO POR AHORA CAMBIAR A TABLA                           #
###############################################################################################

df_fre.to_csv('csv/data_mart_frecuencia_neumococo_10.csv', sep = '|', index = False, encoding = 'latin1')

df_mart = pd.read_csv("csv/data_mart_frecuencia_neumococo_10.csv", sep = '|', encoding = 'latin1')

