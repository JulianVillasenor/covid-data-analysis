import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df_2020 = pd.read_csv('data/COVID19_2020_CONFIRMADOS.csv')
df_2021 = pd.read_csv('data/COVID19_2021_CONFIRMADOS.csv')
df_2022 = pd.read_csv('data/COVID19_2022_CONFIRMADOS.csv')

df_2020 = df_2020[df_2020['ENTIDAD_RES'] == 10]
df_2021 = df_2021[df_2021['ENTIDAD_RES'] == 10]
df_2022 = df_2022[df_2022['ENTIDAD_RES'] == 10]

df_2020['YEAR'] = 2020
df_2021['YEAR'] = 2021
df_2022['YEAR'] = 2022

# Combine datasets
df = pd.concat([df_2020, df_2021, df_2022], ignore_index=True)

# Convert dates to datetime format
df['FECHA_SINTOMAS'] = pd.to_datetime(df['FECHA_SINTOMAS'], errors='coerce')
df['FECHA_DEF'] = pd.to_datetime(df['FECHA_DEF'], errors='coerce')

# Set Streamlit page config
st.set_page_config(page_title="COVID-19 Data Dashboard", layout="wide")

# Title
st.title("COVID-19 Data Dashboard")

# Year selection
years = ['Todos'] + sorted(df['YEAR'].unique().tolist())
selected_year = st.selectbox("Selecciona un año", years)

# Filter data by year
if selected_year == 'Todos':
    filtered_df = df
else:
    filtered_df = df[df['YEAR'] == int(selected_year)]

# Metrics
total_casos = len(filtered_df)
total_fallecimientos = filtered_df['FECHA_DEF'].notna().sum()
total_mujeres = filtered_df[filtered_df['SEXO'] == 2].shape[0]
total_hombres = filtered_df[filtered_df['SEXO'] == 1].shape[0]

# Display metrics
st.subheader("Resumen")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Casos", total_casos)
col2.metric("Total de Fallecimientos", total_fallecimientos)
col3.metric("Total de Mujeres", total_mujeres)
col4.metric("Total de Hombres", total_hombres)

# Bar chart: Evolution of cases by symptom date
cases_by_date = filtered_df.groupby('FECHA_SINTOMAS').size().reset_index(name='Casos')
fig = px.bar(
    cases_by_date,
    x='FECHA_SINTOMAS',
    y='Casos',
    title='Evolución de Casos Confirmados por Fecha de Inicio de Síntomas',
    labels={'FECHA_SINTOMAS': 'Fecha de Inicio de Síntomas', 'Casos': 'Número de Casos'},
    template='plotly_white'
)
st.plotly_chart(fig, use_container_width=True)

# Summary table for age by gender
summary_data = filtered_df.groupby('SEXO')['EDAD'].agg(
    Media='mean',
    Mediana='median',
    Mínimo='min',
    Máximo='max',
    Desviacion='std',
    Q1=lambda x: x.quantile(0.25),
    Q3=lambda x: x.quantile(0.75)
).reset_index()
summary_data['Grupo'] = summary_data['SEXO'].replace({1: 'Hombres', 2: 'Mujeres'})
summary_data = summary_data[['Grupo', 'Media', 'Mediana', 'Mínimo', 'Máximo', 'Desviacion', 'Q1', 'Q3']]

st.subheader("Resumen de la Variable Edad")
st.dataframe(summary_data)
