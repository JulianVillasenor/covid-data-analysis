import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
from dash import dash_table


# Carga los datos
df_2020 = pd.read_csv('data/COVID19_2020_CONFIRMADOS.csv')
df_2021 = pd.read_csv('data/COVID19_2021_CONFIRMADOS.csv')
df_2022 = pd.read_csv('data/COVID19_2022_CONFIRMADOS.csv')

df_2020 = df_2020[df_2020['ENTIDAD_RES'] == 10]
df_2021 = df_2021[df_2021['ENTIDAD_RES'] == 10]
df_2022 = df_2022[df_2022['ENTIDAD_RES'] == 10]


df_2020['YEAR'] = 2020
df_2021['YEAR'] = 2021
df_2022['YEAR'] = 2022

# Unificar los datasets
df = pd.concat([df_2020, df_2021, df_2022], ignore_index=True)

# Convertir fechas a formato datetime
df['FECHA_SINTOMAS'] = pd.to_datetime(df['FECHA_SINTOMAS'], errors='coerce')
df['FECHA_DEF'] = pd.to_datetime(df['FECHA_DEF'], errors='coerce')

# Inicializar la app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la app
app.layout = dbc.Container([
    html.H1("COVID-19 Data Dashboard", className="text-center mb-4"),
    # Filtro por año
    dcc.Dropdown(
        id='year-selector',
        options=[{'label': 'Todos', 'value': 'Todos'}] +
                [{'label': year, 'value': year} for year in df['YEAR'].unique()],
        value='Todos',
        multi=False,
        placeholder="Select a year",
        className="mb-4"
    ),
    # Resumen (Boxen)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Casos", className="card-title"),
                html.H2(id='total-casos', className="card-text")
            ])
        ], color="primary", inverse=True), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Fallecimientos", className="card-title"),
                html.H2(id='total-fallecimientos', className="card-text")
            ])
        ], color="danger", inverse=True), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Mujeres", className="card-title"),
                html.H2(id='total-mujeres', className="card-text")
            ])
        ], color="info", inverse=True), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Hombres", className="card-title"),
                html.H2(id='total-hombres', className="card-text")
            ])
        ], color="success", inverse=True), width=3)
    ], className="mb-4"),
    # Diagrama de barras
    dcc.Graph(id='cases-by-date', className="mb-4"),
    # Tabla resumen
    html.H4("Resumen de la Variable Edad", className="text-center mt-4"),
    dash_table.DataTable(
        id='summary-table',
        columns=[
            {'name': 'Grupo', 'id': 'Grupo'},
            {'name': 'Media', 'id': 'Media'},
            {'name': 'Mediana', 'id': 'Mediana'},
            {'name': 'Mínimo', 'id': 'Mínimo'},
            {'name': 'Máximo', 'id': 'Máximo'},
            {'name': 'Desviación Estándar', 'id': 'Desviacion'},
            {'name': 'Q1 (25%)', 'id': 'Q1'},
            {'name': 'Q3 (75%)', 'id': 'Q3'}
        ],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        page_size=10
    )
], fluid=True)

# Callbacks para actualizar los Boxen
@app.callback(
    [Output('total-casos', 'children'),
     Output('total-fallecimientos', 'children'),
     Output('total-mujeres', 'children'),
     Output('total-hombres', 'children'),
     Output('cases-by-date', 'figure'),
     Output('summary-table', 'data')],
    [Input('year-selector', 'value')]
)
def update_metrics(selected_year):
    # Filtrar por año
    if selected_year == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['YEAR'] == int(selected_year)]
    
    # Calcular métricas
    total_casos = len(filtered_df)
    total_fallecimientos = filtered_df['FECHA_DEF'].notna().sum()
    total_mujeres = filtered_df[filtered_df['SEXO'] == 2].shape[0]
    total_hombres = filtered_df[filtered_df['SEXO'] == 1].shape[0]
    
# Gráfico de barras: evolución de casos por fecha de inicio de síntomas
    cases_by_date = filtered_df.groupby('FECHA_SINTOMAS').size().reset_index(name='Casos')
    fig = px.bar(
        cases_by_date,
        x='FECHA_SINTOMAS',
        y='Casos',
        title='Evolución de Casos Confirmados por Fecha de Inicio de Síntomas',
        labels={'FECHA_SINTOMAS': 'Fecha de Inicio de Síntomas', 'Casos': 'Número de Casos'}
    )
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Número de Casos', template='plotly_white')

    # Tabla resumen de EDAD por SEXO
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

    return total_casos, total_fallecimientos, total_mujeres, total_hombres, fig, summary_data.to_dict('records')

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)