import plotly.graph_objects as go
import json
from urllib.request import urlopen
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np


######################
#    INICIO     TAB 1
######################
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
                colorscale='RdBu',
                colorbar_title="Puntaje global promedio"))
fig.update_layout(mapbox_style="carto-positron",
                    mapbox_zoom=4,
                    mapbox_center = {"lat": 4.570868, "lon": -74.2973328},                        
                    height=700)

fig.update_layout(transition_duration=500)

######################
#    INICIO     TAB 2
######################

df1 = pd.read_excel('D:/UNIANDES/ACTD/Git/Repositorio3/ACTD_Proyecto_3/opciones.xlsx')
opciones = []
columnas = df1.shape[1]
for num in range(1, columnas):
    la_lista=df1.iloc[:,num].dropna().unique()
    #unique_values = list(set(la_lista))
    #sorted_values = sorted(la_lista)
    #lista_ordenada = sorted(list(df1.iloc[:,num].unique()))
    #lista_ordenada = sorted(la_lista, key=lambda x: (x == '', x))
    #lista_ordenada = sorted(lista)
    #lista_sin_vacios = la_lista.remove("NAN")
    #lista_sin_vacios = opciones[~np.isnan(vector)]
    #without_nan = vector[~np.isnan(vector)]
    #lista_sin_vacios = list(set(filter(None, list(df1.iloc[:,num].unique()))))
    #lista_sin_vacios = la_lista[la_lista != ""]
    #print(sorted_values)
    opciones.append(la_lista)

#print(opciones)

app = Dash(__name__)

app._favicon = ('favicon.ico') #must be in /assets/favicon.ico 
app.title = "PROYECTO 3 ACTD"

app.layout = html.Div([    

    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Pestaña 1', value='tab-1', children=[
            
            dbc.Col([
                 
                 html.Br(),
                 #html.Br(),
                dbc.Row(html.Div("PUNTAJE PROMEDIO EN PRUEBAS SABER 11 POR DEPARTAMENTO", style={'fontSize': '24px', 'text-align':'center'})),
                dbc.Row(dcc.Graph(id='graph-with-slider',figure=fig)),
                #dbc.Row(html.Div(["Seleccione el año que quiera visualizar",])),
                dbc.Row(html.Div("Selecciona el año que deseas visualizar", style={'fontSize': '24px', 'text-align':'center'})),
                html.Br(), 
                dcc.Slider(
                    df0['Anio'].astype(int).min(),
                    df0['Anio'].astype(int).max(),
                    step=None,
                    value=df0['Anio'].astype(int).max(),
                    marks={str(year): str(year) for year in df0['Anio'].unique()},
                    id='year-slider'
                ) 
            ],align="center"),
              ]),
        dcc.Tab(label='Pestaña 2', value='tab-2', children=[
             
            dbc.Col([
                dbc.Row(
                    dbc.Col([
                        html.Div(["¿Cuál es el rango de edad?",dcc.Dropdown(id='dropdownAge',options=opciones[0]),])
                    ], width=4),
                    ), #,persistence=True, persistence_type='session'
                dbc.Row(
                    dbc.Col([
                    html.Div(["¿Cuál es el sexo biológico?",
                    dcc.Dropdown(id='dropdownSex',options=opciones[1],value='',),])
                    ]),
                    ),
                dbc.Row(
                    dbc.Col([ 
                    html.Div(["¿Qué tipo de dolor de pecho?",
                    dcc.Dropdown(id='dropdownCPT',options=opciones[2],value='',),])
                    ]),
                    ), 
            ], width=4),

            dbc.Col([
                dbc.Row(
                    html.Div(["¿Cuál es el rango de edad?",
                    dcc.Dropdown(id='dropdownAge',options=opciones[3]),])), #,persistence=True, persistence_type='session'
                dbc.Row(
                    html.Div(["¿Cuál es el sexo biológico?",
                    dcc.Dropdown(id='dropdownSex',options=opciones[4],value='',),])),
                dbc.Row(
                    html.Div(["¿Qué tipo de dolor de pecho?",
                    dcc.Dropdown(id='dropdownCPT',options=opciones[5],value='',),])), 
            ], width=4),

                            
                # dbc.Col(
                #     html.Div(["¿Cuál representa la presion arterial en reposo?",
                #     dcc.Dropdown(id='dropdowntrestbps',options=opttrestbps,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(["¿Cuál es el nivel de colesterol?",
                #     dcc.Dropdown(id='dropdownchol',options=optchol,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(["¿Cuál es el nivel de Azucar en la sangre?",
                #     dcc.Dropdown(id='dropdownfbs',options=optfbs,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(["¿Cuál fue el resultados del electrogardiografo?",
                #     dcc.Dropdown(id='dropdownrestecg',options=optrestecg,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(["¿Cuál ha sido su Maximo ritmo cardiaco?",
                #     dcc.Dropdown(id='dropdownthalach',options=optthalach,value='',),]),width=4),
                #     dbc.Col(
                #     html.Div(["¿Presenta Angina producida por ejercicio?",
                #     dcc.Dropdown(id='dropdownexang',options=optexang,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(["¿Cuál es la depresion ST relativo al reposo?",
                #     dcc.Dropdown(id='dropdownoldpeak',options=optoldpeak,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(["¿Cuál es el Segmento ST peak?",
                #     dcc.Dropdown(id='dropdownslope',options=optslope,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(["¿Cuánto es el número de mayores vasos sanguineos?",
                #     dcc.Dropdown(id='dropdownca',options=optca,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(["¿Cuál esel  valor de thalasemia?",
                #     dcc.Dropdown(id='dropdownthal',options=optthal,value='',),]),width=4),
                # dbc.Col(
                #     html.Div(id='OutRespuesta',),width=4),
            
            ]),
        dcc.Tab(label='Pestaña 3', value='tab-3', ),
    ]),



    
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    #Output('page-content', 'children'),
    Input('year-slider', 'value'))
    #Input('url','pathname'))
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
                        colorscale='RdBu'
                        #colorbar_title="Puntaje global promedio"
                        ))
        fig.update_layout(mapbox_style="carto-positron",
                            mapbox_zoom=4.5,
                            mapbox_center = {"lat": 4.570868, "lon": -74.2973328},
                            height=700)

        fig.update_layout(transition_duration=500)

        return fig





if __name__ == '__main__':
    app.run_server(debug=True)
    