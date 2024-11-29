import pandas as pd
import streamlit as st
import plotly.express as px

# Preparar datos
df = pd.read_csv('data/COVID19_CONFIRMADOS.csv')

# Configurar página
st.set_page_config(page_title="COVID-19 Data Dashboard", layout="wide")

st.title("Visualizacion de datos COVID-19 en Durango")

# *******************************************************************************
# Filtro por año (todos, 2020, 2021, 2022)
# *******************************************************************************

years = ['Todos'] + sorted(df['YEAR'].unique().tolist())
selected_year = st.selectbox("Selecciona un año", years)

if selected_year == 'Todos':
    filtered_df = df
else:
    filtered_df = df[df['YEAR'] == int(selected_year)]

# *******************************************************************************
# Total de casos por el filtro de año elegido, total de fallecimientos, total de mujeres y total de hombres.
# *******************************************************************************

total_casos = len(filtered_df)
total_fallecimientos = filtered_df['FECHA_DEF'].notna().sum()
total_mujeres = filtered_df[filtered_df['SEXO'] == 2].shape[0]
total_hombres = filtered_df[filtered_df['SEXO'] == 1].shape[0]

st.subheader("Resumen")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Casos", total_casos)
col2.metric("Total de Fallecimientos", total_fallecimientos)
col3.metric("Total de Mujeres", total_mujeres)
col4.metric("Total de Hombres", total_hombres)

# *******************************************************************************
# Diagrama de barras para la evolución de casos confirmados por fecha de inicio de sintomas
# *******************************************************************************

cases_by_date = filtered_df.groupby('FECHA_SINTOMAS').size().reset_index(name='Casos')
fig_cases_by_date = px.bar(
    cases_by_date,
    x='FECHA_SINTOMAS',
    y='Casos',
    title='Evolución de Casos Confirmados por Fecha de Inicio de Síntomas',
    labels={'FECHA_SINTOMAS': 'Fecha de Inicio de Síntomas', 'Casos': 'Número de Casos'},
    template='plotly_white'
)
st.plotly_chart(fig_cases_by_date, use_container_width=True)

# *******************************************************************************
# Tabla resumen de la variable Edad por Sexo o por Tipo Paciente (media, mediana, cuartiles, minimo, maximo, desviación estándar).
# *******************************************************************************

table_by_Sexo_Edad = filtered_df.groupby('SEXO')['EDAD'].agg(
    Media=lambda x: round(x.mean(), 2), 
    Mediana='median',
    Mínimo='min',
    Máximo='max',
    Desviacion=lambda x: round(x.std(), 2),
    Q1=lambda x: x.quantile(0.25),
    Q3=lambda x: x.quantile(0.75)
).reset_index()
table_by_Sexo_Edad['Grupo'] = table_by_Sexo_Edad['SEXO'].replace({1: 'Hombres', 2: 'Mujeres'})
table_by_Sexo_Edad = table_by_Sexo_Edad[['Grupo', 'Media', 'Mediana', 'Mínimo', 'Máximo', 'Desviacion', 'Q1', 'Q3']]

table_by_TipoPaciente_Edad = filtered_df.groupby('TIPO_PACIENTE')['EDAD'].agg(
    Media=lambda x: round(x.mean(), 2), 
    Mediana='median',
    Mínimo='min',
    Máximo='max',
    Desviacion=lambda x: round(x.std(), 2),
    Q1=lambda x: x.quantile(0.25),
    Q3=lambda x: x.quantile(0.75)
).reset_index()
table_by_TipoPaciente_Edad['Tipo de paciente'] = table_by_TipoPaciente_Edad['TIPO_PACIENTE'].replace({1: 'Ambulatorio', 2: 'Hospitalizado'})
table_by_TipoPaciente_Edad = table_by_TipoPaciente_Edad[['Tipo de paciente', 'Media', 'Mediana', 'Mínimo', 'Máximo', 'Desviacion', 'Q1', 'Q3']]

# Mostrar ambos gráficos en dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Metricas de la edad de los pacientes por tipo de sexo")
    st.dataframe(table_by_Sexo_Edad, hide_index=True)

with col2:
    st.subheader("Metricas de la edad de los pacientes por tipo de paciente")
    st.dataframe(table_by_TipoPaciente_Edad, hide_index=True)

# *******************************************************************************
# Diagrama de barras apiladas
# *******************************************************************************

# Crear dataframe con proporciones de casos y defunciones por tipo de paciente y sexo
grouped_by_TipoPaciente_Sexo = filtered_df.groupby(['TIPO_PACIENTE', 'SEXO']).agg(
    CASOS=('TIPO_PACIENTE', 'size'),  # Total de casos
    DEFUNCIONES=('FECHA_DEF', lambda x: x.notnull().sum())  # Total de defunciones
).reset_index()

# Calcular el total de casos y defunciones por TIPO_PACIENTE
total_casos = grouped_by_TipoPaciente_Sexo.groupby('TIPO_PACIENTE')['CASOS'].transform('sum')
total_defunciones = grouped_by_TipoPaciente_Sexo.groupby('TIPO_PACIENTE')['DEFUNCIONES'].transform('sum')

# Calcular las proporciones
grouped_by_TipoPaciente_Sexo['PROPORCION_TOTAL_CASOS'] = grouped_by_TipoPaciente_Sexo['CASOS'] / total_casos
grouped_by_TipoPaciente_Sexo['PROPORCION_TOTAL_DEFUNCIONES'] = grouped_by_TipoPaciente_Sexo['DEFUNCIONES'] / total_defunciones

# Reemplazar valores de TIPO_PACIENTE y SEXO por etiquetas descriptivas
grouped_by_TipoPaciente_Sexo['TIPO_PACIENTE'] = grouped_by_TipoPaciente_Sexo['TIPO_PACIENTE'].replace({
    1: 'Ambulatorio',
    2: 'Hospitalizado'
})
grouped_by_TipoPaciente_Sexo['SEXO'] = grouped_by_TipoPaciente_Sexo['SEXO'].replace({
    1: 'Hombre',
    2: 'Mujer'
})

# Diagrama de barras apiladas de la proporcion de casos por tipo de paciente segun su sexo
fig_stacked_1 = px.bar(
    grouped_by_TipoPaciente_Sexo,
    x='PROPORCION_TOTAL_CASOS',
    y='TIPO_PACIENTE',
    color='SEXO',
    orientation='h',  # Barras horizontales
    title='Distribución de casos por Tipo de Paciente y Sexo',
    labels={
        'PROPORCION_TOTAL_CASOS': 'Proporción (%)',
        'TIPO_PACIENTE': 'Tipo de Paciente',
        'SEXO': 'Sexo'
    },
    barmode='stack',
    template='plotly_white'
)

# Ajustar formato de la gráfica
fig_stacked_1.update_layout(
    xaxis_tickformat='.0%',  # Mostrar el eje X como porcentaje
    xaxis_title='Proporción',
    yaxis_title='Tipo de Paciente',
    legend_title=None,
    showlegend=False,  # Ocultar completamente las leyendas
)

# Diagrama de barras apiladas de la proporcion de defunciones por tipo de paciente segun su sexo
fig_stacked_2 = px.bar(
    grouped_by_TipoPaciente_Sexo,
    x='PROPORCION_TOTAL_DEFUNCIONES',
    y='TIPO_PACIENTE',
    color='SEXO',
    orientation='h',  # Barras horizontales
    title='Proporción de Defunciones por Tipo de Paciente y Sexo',
    labels={
        'PROPORCION_TOTAL_DEFUNCIONES': 'Proporción de Defunciones',
        'TIPO_PACIENTE': 'Tipo de Paciente',
        'SEXO': 'Sexo'
    },
    barmode='stack',
    template='plotly_white'
)

# Ajustar formato del eje X para porcentajes
fig_stacked_2.update_layout(
    xaxis_tickformat='.0%',  # Mostrar proporciones en formato porcentual
    xaxis_title='Proporción',
    yaxis_title=None,
    legend_title='Sexo',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Mostrar ambos gráficos en dos columnas
with col1:
    st.plotly_chart(fig_stacked_1, use_container_width=True)

with col2:
    st.plotly_chart(fig_stacked_2, use_container_width=True)

# *******************************************************************************
# Diagramas circulares para las comorbilidades
# *******************************************************************************

st.subheader("Distribuciones por comorbilidad")

# Limpieza global de las comorbilidades
df['TABAQUISMO'] = df['TABAQUISMO'].replace({2: 0, 98: 0})  # Considerar 98 como "No Fuma"
df['DIABETES'] = df['DIABETES'].replace({2: 0, 98: 0})      # Considerar 98 como "Sin Diabetes"
df['OBESIDAD'] = df['OBESIDAD'].replace({2: 0, 98: 0})      # Considerar 98 como "Sin Obesidad"
df['HIPERTENSION'] = df['HIPERTENSION'].replace({2: 0, 98: 0})  # Considerar 98 como "Sin Hipertensión"

# Elimina filas con valores nulos en las comorbilidades
df = df.dropna(subset=['TABAQUISMO', 'DIABETES', 'OBESIDAD', 'HIPERTENSION'])

# Función para generar diagramas circulares
def generate_pie_chart(data, column, title, labels_dict):
    counts = data[column].value_counts()  # Cuenta los valores 0 y 1
    labels = [labels_dict.get(value, f"Desconocido ({value})") for value in counts.index]
    return px.pie(
        values=counts.values,
        names=labels,
        title=title,
        color_discrete_sequence=px.colors.sequential.Agsunset
    )

# Diccionarios de etiquetas para cada comorbilidad
labels_tabaquismo = {0: 'No Fuma', 1: 'Fuma'}
labels_diabetes = {0: 'Sin Diabetes', 1: 'Con Diabetes'}
labels_obesidad = {0: 'Sin Obesidad', 1: 'Con Obesidad'}
labels_hipertension = {0: 'Sin Hipertensión', 1: 'Con Hipertensión'}

# Mostrar gráficos en cuatro columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Diagrama circular para TABAQUISMO
    fig_tabaquismo = generate_pie_chart(filtered_df, 'TABAQUISMO', 'Tabaquismo', labels_tabaquismo)
    st.plotly_chart(fig_tabaquismo, use_container_width=True)

with col2:
    # Diagrama circular para DIABETES
    fig_diabetes = generate_pie_chart(filtered_df, 'DIABETES', 'Diabetes', labels_diabetes)
    st.plotly_chart(fig_diabetes, use_container_width=True)

with col3:
    # Diagrama circular para OBESIDAD
    fig_obesidad = generate_pie_chart(filtered_df, 'OBESIDAD', 'Obesidad', labels_obesidad)
    st.plotly_chart(fig_obesidad, use_container_width=True)

with col4:
    # Diagrama circular para HIPERTENSION
    fig_hipertension = generate_pie_chart(filtered_df, 'HIPERTENSION', 'Hipertensión', labels_hipertension)
    st.plotly_chart(fig_hipertension, use_container_width=True)

# *******************************************************************************
# Boxplot e histogramas para la variable Edad por Sexo y por TipoPaciente
# *******************************************************************************

# Boxplot para la variable Edad por Sexo
fig_boxplot_sexo = px.box(
    filtered_df,
    x='SEXO',
    y='EDAD',
    title='Distribución de edad por sexo',
    labels={'SEXO': 'Sexo', 'EDAD': 'Edad'},
    category_orders={'SEXO': [1, 2]},  # Asegura que los valores de SEXO estén en orden
    color='SEXO',
    color_discrete_map={1: 'blue', 2: 'pink'},  # Colores personalizados para hombres y mujeres
    boxmode='group',
    template='plotly_white'
)

# Ajustar formato de la gráfica
fig_boxplot_sexo.update_layout(
    xaxis_title='Sexo',
    yaxis_title='Edad',
    xaxis=dict(tickvals=[1, 2], ticktext=['Hombres', 'Mujeres']),
    showlegend=False
)

# Boxplot para la variable Edad por Tipo de Paciente
fig_boxplot_tipo_paciente = px.box(
    filtered_df,
    x='TIPO_PACIENTE',
    y='EDAD',
    title='Distribución de Edad por Tipo de Paciente',
    labels={'TIPO_PACIENTE': 'Tipo de Paciente', 'EDAD': 'Edad'},
    category_orders={'TIPO_PACIENTE': [1, 2]},  # Asegura que los valores de TIPO_PACIENTE estén en orden
    color='TIPO_PACIENTE',  # Colorear por tipo de paciente
    color_discrete_map={1: 'orange', 2: 'green'},  # Colores personalizados para ambulatorio y hospitalizado
    boxmode='group',  # Agrupar por categoría
    template='plotly_white'
)

# Ajustar formato de la gráfica
fig_boxplot_tipo_paciente.update_layout(
    xaxis_title='Tipo de Paciente',
    yaxis_title='Edad',
    xaxis=dict(tickvals=[1, 2], ticktext=['Ambulatorio', 'Hospitalizado']),
    showlegend=False  # No mostrar la leyenda
)

# Mostrar ambos gráficos en dos columnas
col1, col2 = st.columns(2)

# Mostrar graficas boxplot en dos columnas
with col1:
    st.plotly_chart(fig_boxplot_sexo, use_container_width=True)

with col2:
    st.plotly_chart(fig_boxplot_tipo_paciente, use_container_width=True)

# *******************************************************************************
# Histogramas para la variable Edad por Sexo
fig_hist_sexo = px.histogram(
    filtered_df,
    x='EDAD',
    color='SEXO',
    title='Distribución de edad por sexo',
    labels={'SEXO': 'Sexo', 'EDAD': 'Edad'},
    category_orders={'SEXO': [1, 2]},  # Asegura que los valores de SEXO estén en orden
    color_discrete_map={1: 'blue', 2: 'pink'},  # Colores personalizados para hombres y mujeres
    nbins=30,  # Número de bins en el histograma
    template='plotly_white'
)

# Ajustar formato del histograma
fig_hist_sexo.update_layout(
    xaxis_title='Edad',
    yaxis_title='Frecuencia',
    barmode='overlay',  # Mostrar las barras superpuestas
    xaxis=dict(range=[0, 100]),  # Rango de edad entre 0 y 100
    legend_title='Sexo',
    bargap=0.02
)

# Cambiar las etiquetas de la leyenda en un histograma
fig_hist_sexo.for_each_trace(
    lambda trace: trace.update(name="Hombres" if trace.name == '1' else "Mujeres")
)

# Histogramas para la variable Edad por Tipo de Paciente
fig_hist_tipo_paciente = px.histogram(
    filtered_df,
    x='EDAD',
    color='TIPO_PACIENTE',
    title='Distribución de Edad por Tipo de Paciente',
    labels={'TIPO_PACIENTE': 'Tipo de Paciente', 'EDAD': 'Edad'},
    category_orders={'TIPO_PACIENTE': [1, 2]},  # Asegura que los valores de TIPO_PACIENTE estén en orden
    color_discrete_map={1: 'orange', 2: 'green'},  # Colores personalizados para ambulatorio y hospitalizado
    nbins=30,  # Número de bins en el histograma
    template='plotly_white'
)

# Ajustar formato del histograma
fig_hist_tipo_paciente.update_layout(
    xaxis_title='Edad',
    yaxis_title='Frecuencia',
    barmode='overlay',  # Mostrar las barras superpuestas
    xaxis=dict(range=[0, 100]),  # Rango de edad entre 0 y 100
    legend_title='Tipo de Paciente',
    bargap=0.02
)

# Cambiar las etiquetas de la leyenda en un histograma
fig_hist_tipo_paciente.for_each_trace(
    lambda trace: trace.update(name="Ambulatorio" if trace.name == '1' else "Hospitalario")
)

# Mostrar graficas histogramas en dos columnas
with col1:
    st.plotly_chart(fig_hist_sexo, use_container_width=True)

with col2:
    st.plotly_chart(fig_hist_tipo_paciente, use_container_width=True)
