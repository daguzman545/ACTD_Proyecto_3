import plotly.graph_objects as go
import json
from urllib.request import urlopen
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc



df0 = pd.read_excel('D:/UNIANDES/ACTD/Git/Repositorio3/ACTD_Proyecto_3/datos8.xlsx',dtype={"cole_cod_mcpio_ubicacion": str,"cole_cod_mcpio_ubicacion":str})
# Se arreglan diferencias entre el df y el json

Anio_seleccionado = 2022

df= df0[df0['Anio'] == Anio_seleccionado]

df = df0.replace('VALLE', 'VALLE DEL CAUCA')
df = df0.replace('NARIÃ‘O', 'NARIÑO') 
df = df0.replace('BOGOTÃ', 'SANTAFE DE BOGOTA D.C') 

with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
    counties = json.load(response)

locs = df['cole_depto_ubicacion']
zs = df['average_column'].round(1)

for loc in counties['features']:
    loc['id'] = loc['properties']['NOMBRE_DPT']

    fig = go.Figure(go.Choroplethmapbox(
                    geojson=counties,
                    locations=locs,
                    z=zs,
                    #colorscale='YlOrRd',                    
                    #colorscale='YlGnBu',
                    colorscale='RdBu',
                    #colorscale='Greys',
                    #colorscale='Blues',
                    #colorscale='Viridis',
                    colorbar_title="Puntaje global promedio"))
    fig.update_layout(mapbox_style="carto-positron",
                        mapbox_zoom=4,
                        mapbox_center = {"lat": 4.570868, "lon": -74.2973328})

    fig.update_layout(transition_duration=500)



app = Dash(__name__)

app.layout = html.Div([    

    dbc.Col([
                dbc.Row(html.Div(["Mapa de Colombia",])),
                dbc.Row(dcc.Graph(id='graph-with-slider',figure=fig)),
                dbc.Row(html.Div(["Seleccione el año que quiera visualizar",])),
    #dcc.Graph(id='graph-with-slider',figure=fig),
    
    #dbc.Row(html.Div(["¿Cuál es el rango de edad?",]),width=4),
                #dbc.Row(dcc.Graph(id='graph-with-slider',figure=fig),width=4),

    #dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df0['Anio'].astype(int).min(),
        df0['Anio'].astype(int).max(),
        step=None,
        value=df0['Anio'].astype(int).min(),
        marks={str(year): str(year) for year in df0['Anio'].unique()},
        id='year-slider'
    )

    ],align="center"),
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    
    df = pd.read_excel('D:/UNIANDES/ACTD/Git/Repositorio3/ACTD_Proyecto_3/datos8.xlsx',dtype={"cole_cod_mcpio_ubicacion": str,"cole_cod_mcpio_ubicacion":str})
    df= df[df['Anio'] == selected_year]

    df = df.replace('VALLE', 'VALLE DEL CAUCA')
    df = df.replace('NARIÃ‘O', 'NARIÑO') 
    df = df.replace('BOGOTÃ', 'SANTAFE DE BOGOTA D.C') 

    locs = df['cole_depto_ubicacion']
    zs = df['average_column'].round(1)
    
    fig = go.Figure(go.Choroplethmapbox(
                    geojson=counties,
                    locations=locs,
                    z=zs,
                    #colorscale='YlOrRd',                    
                    #colorscale='YlGnBu',
                    colorscale='RdBu',
                    #colorscale='Greys',
                    #colorscale='Blues',
                    #colorscale='Viridis',
                    colorbar_title="Puntaje global promedio"))
    fig.update_layout(mapbox_style="carto-positron",
                        mapbox_zoom=4,
                        mapbox_center = {"lat": 4.570868, "lon": -74.2973328})

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)