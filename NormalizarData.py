# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 09:10:41 2024

@author: Rodrigo
"""

import pandas as pd

# Ruta del archivo
path_file = 'csv/Dataset_vacunacion_clean.csv'

# Instanciar DF
df_vacunacion = pd.read_csv(path_file, sep = '|', encoding = 'latin1')

# Reemplazar datos na en la columna GrupoEtnico por "Ninguno de los anteriores"
df_vacunacion['GrupoEtnico'] = df_vacunacion['GrupoEtnico'].fillna('Ninguno de los anteriores')

# Crear un diccionario para mapear los valores
sex_map = {'Hombre': 1, 'Mujer': 2}

# Aplicar la transformación
df_vacunacion['Sexo'] = df_vacunacion['Sexo'].map(sex_map)

# Generar archivo CSV con data normalizada
df_vacunacion.to_csv('csv/Dataset_vacunacion_normalizada.csv', sep = '|', index = False, encoding = 'latin1')