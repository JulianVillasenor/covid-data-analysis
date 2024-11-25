import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

# Carga los datos
data_2020 = pd.read_csv('data/COVID19_2020_CONFIRMADOS.csv')
data_2021 = pd.read_csv('data/COVID19_2021_CONFIRMADOS.csv')
data_2022 = pd.read_csv('data/COVID19_2022_CONFIRMADOS.csv')

# Unificar los datasets
data = pd.concat([data_2020, data_2021, data_2022], ignore_index=True)

# Convertir fechas a formato datetime
data['FECHA_SINTOMAS'] = pd.to_datetime(data['FECHA_SINTOMAS'])
data['Año'] = data['FECHA_SINTOMAS'].dt.year

# Inicializar la app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la aplicación
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard COVID-19", className="text-center text-primary mb-4"))
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='year-filter',
                options=[
                    {'label': 'Todos', 'value': 'Todos'},
                    {'label': '2020', 'value': 2020},
                    {'label': '2021', 'value': 2021},
                    {'label': '2022', 'value': 2022}
                ],
                value='Todos',
                placeholder="Seleccione un año",
                className="mb-3"
            )
        ])
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='summary-box'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='cases-bar-chart'), width=12)
    ])
])

# Callbacks para actualizar las visualizaciones
@app.callback(
    [Output('summary-box', 'children'),
     Output('cases-bar-chart', 'figure')],
    [Input('year-filter', 'value')]
)
def update_dashboard(year):
    # Filtrar datos según el año seleccionado
    if year == 'Todos':
        filtered_data = data
    else:
        filtered_data = data[data['Año'] == int(year)]

    # Calcular totales
    total_cases = len(filtered_data)
    total_deaths = filtered_data['FECHA_DEF'].notna().sum()
    total_women = (filtered_data['SEXO'] == 2).sum()  # Asumiendo 2 = Mujeres
    total_men = (filtered_data['SEXO'] == 1).sum()    # Asumiendo 1 = Hombres

    # Crear un resumen
    summary = dbc.Card(
        dbc.CardBody([
            html.H4(f"Casos Confirmados: {total_cases}"),
            html.H4(f"Fallecimientos: {total_deaths}"),
            html.H4(f"Mujeres: {total_women}"),
            html.H4(f"Hombres: {total_men}")
        ]),
        className="mb-4"
    )

    # Diagrama de barras
    bar_chart = px.bar(
        filtered_data.groupby('FECHA_SINTOMAS')['ID_REGISTRO'].count().reset_index(),
        x='FECHA_SINTOMAS',
        y='ID_REGISTRO',
        title='Evolución de Casos Confirmados por Fecha de Inicio de Síntomas',
        labels={'ID_REGISTRO': 'Número de Casos'}
    )

    return summary, bar_chart

# Ejecutar la app
if __name__ == "__main__":
    app.run_server(debug=True)
