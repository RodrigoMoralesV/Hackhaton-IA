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
    query = "SELECT * FROM pacientes limit 10000"
    data = pd.read_sql_query(query, conn)

    # Mostrar las primeras filas del DataFrame
    print(data.head())

except Exception as e:
    print(f"Error al conectarse a la base de datos: {e}")

finally:
    if conn:
        conn.close()  # Cierra la conexión a la base de datos

data['edad'] = (datetime.now() - pd.to_datetime(data['fecnac'])).dt.days // 365
