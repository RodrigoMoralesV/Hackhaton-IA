# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 09:07:43 2024

@author: Rodrigo
"""

## Preguntas
# Numero de personas que han recibido la segunda dosis de la vacuna neumococo
# Cantidad de personas que recibieron la vacuna de refuerzo
# ¿Cuántas personas han recibido la primera dosis de la vacuna de neumococo?
# ¿Cuál es el porcentaje de la población que tiene al menos una dosis?
# Cuantas personas NO han recibido alguna dosis de vacuna neumococo conjugado 10 valente?

import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Configura tu API key de OpenAI
openai.api_key = os.getenv('API_KEY')

# Cargar el CSV
df = pd.read_csv('csv/data_mart_frecuencia_neumococo_10.csv', sep='|', encoding='latin1')

# Función para calcular el porcentaje de vacunación
def calcular_porcentaje_vacunacion():
    total_poblacion = len(df)
    al_menos_una_dosis = df['neumococo_conjugado_10_valente_primera'].notna().sum()
    porcentaje = (al_menos_una_dosis / total_poblacion) * 100
    return porcentaje

# Función para calcular esquemas completos
def calcular_esquemas_completos():
    esquemas_completos = df[
        (df['neumococo_conjugado_10_valente_primera'].notna()) &
        (df['neumococo_conjugado_10_valente_segunda'].notna()) &
        (df['neumococo_conjugado_10_valente_refuerzo'].notna())
    ]
    return len(esquemas_completos)

# Función para calcular la frecuencia de vacunación
def calcular_frecuencia_vacunacion():
    frecuencia_general = df['frecuencia_vacunacion'].value_counts()
    return frecuencia_general

# Función para buscar personas discapacitadas que han recibido la vacuna
def personas_discapacitadas_con_vacuna():
    discapacitados = df[df['discapacitado'].str.upper() == 'SI']
    return len(discapacitados[discapacitados['neumococo_conjugado_10_valente_primera'].notna()])

# Función para buscar en CSV según la pregunta
def buscar_en_csv(pregunta_interpretada):
    if 'primera dosis' in pregunta_interpretada.lower():
        total_primera = df['neumococo_conjugado_10_valente_primera'].notna().sum()
        return f"El número de personas que han recibido la primera dosis de la vacuna de neumococo es: {total_primera}"

    elif 'segunda dosis' in pregunta_interpretada.lower():
        total_segunda = df['neumococo_conjugado_10_valente_segunda'].notna().sum()
        return f"El número de personas que han recibido la segunda dosis de la vacuna de neumococo es: {total_segunda}"

    elif 'refuerzo' in pregunta_interpretada.lower():
        total_refuerzo = df['neumococo_conjugado_10_valente_refuerzo'].notna().sum()
        return f"El número de personas que han recibido la vacuna de refuerzo de neumococo es: {total_refuerzo}"

    elif 'ninguna dosis' in pregunta_interpretada.lower():
        total_ninguna = df[df['neumococo_conjugado_10_valente_primera'].isna()].shape[0]
        return f"El número de personas que no han recibido ninguna dosis es: {total_ninguna}"

    elif 'intervalo promedio' in pregunta_interpretada.lower():
        return "No se ha implementado el cálculo del intervalo promedio."

    elif 'esquema completo' in pregunta_interpretada.lower():
        total_completos = calcular_esquemas_completos()
        return f"El número de personas con el esquema completo de vacunación es: {total_completos}"

    elif 'porcentaje' in pregunta_interpretada.lower():
        porcentaje = calcular_porcentaje_vacunacion()
        return f"El porcentaje de la población que tiene al menos una dosis es: {porcentaje:.2f}%"

    elif 'bogotá' in pregunta_interpretada.lower() and 'segunda dosis' in pregunta_interpretada.lower():
        total_bogota_segunda = df[
            (df['nombremunicipioresidencia'].str.contains('BOGOTÁ', case=False)) &
            (df['neumococo_conjugado_10_valente_segunda'].notna())
        ].shape[0]
        return f"El número de personas en Bogotá, D.C. que han recibido la segunda dosis es: {total_bogota_segunda}"

    elif 'frecuencia' in pregunta_interpretada.lower():
        frecuencia = calcular_frecuencia_vacunacion()
        return f"La frecuencia de vacunación general es:\n{frecuencia}"

    elif 'discapacitados' in pregunta_interpretada.lower():
        total_discapacitados = personas_discapacitadas_con_vacuna()
        return f"El número de personas discapacitadas que han recibido la vacuna de neumococo es: {total_discapacitados}"

    elif 'intervalo promedio entre segunda dosis' in pregunta_interpretada.lower():
        return "No se ha implementado el cálculo del intervalo promedio entre dosis."

    elif 'municipio con mayor número de personas' in pregunta_interpretada.lower():
        municipio_mayor = df['nombremunicipioresidencia'].value_counts().idxmax()
        total_mayor = df['nombremunicipioresidencia'].value_counts().max()
        return f"El municipio con mayor número de personas con el esquema completo es: {municipio_mayor} con {total_mayor} personas."

    return "Lo siento, no encontré información relevante."

# Función para interpretar la pregunta usando GPT
def interpretar_pregunta(pregunta):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente que ayuda a interpretar preguntas sobre esquemas de vacunación."},
            {"role": "user", "content": f"Interpreta la siguiente pregunta y devuelve un resumen de la información solicitada: {pregunta}"}
        ],
        max_tokens=100
    )
    return response['choices'][0]['message']['content'].strip()

# Función principal para obtener la respuesta
def obtener_respuesta(pregunta):
    pregunta_interpretada = interpretar_pregunta(pregunta)
    respuesta = buscar_en_csv(pregunta_interpretada)
    return respuesta

# Función principal del chatbot
def main():
    print("¡Hola! Soy tu chatbot sobre esquemas de vacunación. ¿Cómo puedo ayudarte hoy?")
    while True:
        pregunta = input("Tú: ")
        if pregunta.lower() in ['salir', 'exit', 'q', 'quit']:
            print("¡Hasta luego!")
            break
        
        respuesta = obtener_respuesta(pregunta)
        print("Bot:", respuesta)

if __name__ == "__main__":
    main()