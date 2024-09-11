import pandas as pd
import psycopg2
from datetime import datetime

# Datos de la conexión
dbname = "db_vacunacion"
user = "postgres"
password = "1234"
host = "localhost"
port = "5432"

data= {}

# Establecer la conexión con la base de datos
try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Conexión exitosa a la base de datos")

    # Cargar datos de la tabla 'pacientes' a un DataFrame de pandas
    query = """select 
                    FechaNacimiento,
                	covid_sinovac_primera,
                	covid_sinovac_segunda,
                	covid_sinovac_refuerzo,
                	covid_sinovac_primer_refuerzo,
                	covid_sinovac_segundo_refuerzo,
                	covid_pfizer_primera,
                	covid_pfizer_segunda,
                	covid_pfizer_refuerzo,
                	covid_pfizer_primer_refuerzo,
                	covid_pfizer_segundo_refuerzo,
                	covid_moderna_primera,
                	covid_moderna_segunda,
                	covid_moderna_refuerzo,
                	covid_moderna_primer_refuerzo,
                	covid_moderna_segundo_refuerzo,
                	covid_janssen_unica,
                	covid_janssen_segunda,
                	covid_janssen_refuerzo,
                	covid_janssen_primer_refuerzo,
                	covid_janssen_segundo_refuerzo,
                	covid_astrazeneca_primera,
                	covid_astrazeneca_segunda,
                	covid_astrazeneca_refuerzo,
                	covid_astrazeneca_primer_refuerzo,
                	covid_astrazeneca_segundo_refuerzo,
                	covid_moderna_pediatrica_primera,
                	covid_moderna_pediatrica_segunda,
                	covid_pfizer_adicional
                from 
                	data_lake_vacunacion
                where
                	FechaNacimiento is not null and TipoIdentificacion = 'RC';
            """
    data = pd.read_sql_query(query, conn)

    # Mostrar las primeras filas del DataFrame
    print(data.head())

except Exception as e:
    print(f"Error al conectarse a la base de datos: {e}")

finally:
    if conn:
        conn.close()  # Cierra la conexión a la base de datos

data['edad'] = (datetime.now() - pd.to_datetime(data['fechanacimiento'])).dt.days // 365
