import pandas as pd
import numpy as np

# Ubicación del archivo
path_file = 'data/data_mart_frecuencia_vacunacion.csv'

# Lectura del archivo
df = pd.read_csv(path_file, sep='|', encoding='latin1')

# Declarar columnas a extraer
columnas_extraidas = [
    'tipoidentificacion',
    'fechanacimiento', 'covid_sinovac_primera',
    'covid_sinovac_segunda',
    'covid_sinovac_refuerzo',
    'covid_sinovac_primer_refuerzo',
    'covid_sinovac_segundo_refuerzo',
    'covid_pfizer_primera',
    'covid_pfizer_segunda',
    'covid_pfizer_refuerzo',
    'covid_pfizer_primer_refuerzo',
    'covid_pfizer_segundo_refuerzo',
    'covid_moderna_primera',
    'covid_moderna_segunda',
    'covid_moderna_refuerzo',
    'covid_moderna_primer_refuerzo',
    'covid_moderna_segundo_refuerzo',
    'covid_janssen_unica',
    'covid_janssen_segunda',
    'covid_janssen_refuerzo',
    'covid_janssen_primer_refuerzo',
    'covid_janssen_segundo_refuerzo',
    'covid_astrazeneca_primera',
    'covid_astrazeneca_segunda',
    'covid_astrazeneca_refuerzo',
    'covid_astrazeneca_primer_refuerzo',
    'covid_astrazeneca_segundo_refuerzo',
    'covid_moderna_pediatrica_primera',
    'covid_moderna_pediatrica_segunda',
    'covid_pfizer_adicional']

# Obtener las columnas son necesarias
df_fre = df[columnas_extraidas]

# Declarar las vacunas a analizar
columnas_vacunas = ['covid_sinovac_primera',
                    'covid_sinovac_segunda',
                    'covid_sinovac_refuerzo',
                    'covid_sinovac_primer_refuerzo',
                    'covid_sinovac_segundo_refuerzo',
                    'covid_pfizer_primera',
                    'covid_pfizer_segunda',
                    'covid_pfizer_refuerzo',
                    'covid_pfizer_primer_refuerzo',
                    'covid_pfizer_segundo_refuerzo',
                    'covid_moderna_primera',
                    'covid_moderna_segunda',
                    'covid_moderna_refuerzo',
                    'covid_moderna_primer_refuerzo',
                    'covid_moderna_segundo_refuerzo',
                    'covid_janssen_unica',
                    'covid_janssen_segunda',
                    'covid_janssen_refuerzo',
                    'covid_janssen_primer_refuerzo',
                    'covid_janssen_segundo_refuerzo',
                    'covid_astrazeneca_primera',
                    'covid_astrazeneca_segunda',
                    'covid_astrazeneca_refuerzo',
                    'covid_astrazeneca_primer_refuerzo',
                    'covid_astrazeneca_segundo_refuerzo',
                    'covid_moderna_pediatrica_primera',
                    'covid_moderna_pediatrica_segunda',
                    'covid_pfizer_adicional']

# Aseguramos que las fechas sean tipo datetime
df_fre.loc[:, 'fechanacimiento'] = pd.to_datetime(df['fechanacimiento'], errors='coerce')

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

# Creamos una nueva columna que contenga la cantidad de vacunas aplicadas antes de los 5 años
df_fre['vacunas_0_a_5'] = df_fre.apply(contar_vacunas, axis=1)

# Verificamos el resultado
print(df_fre[['tipoidentificacion', 'fechanacimiento', 'vacunas_0_a_5']].head())
