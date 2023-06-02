import psycopg2
import pandas as pd
import seaborn as sns

import plotly.graph_objects as go
import json
from urllib.request import urlopen
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
#import numpy as np
import plotly.express as px

######################
#    INICIO     MODELO
######################

from pgmpy.readwrite import XMLBIFReader
import pandas as pd

#Se lee el modelo
reader = XMLBIFReader("modeloM5CL.xml")
modelo = reader.get_model()

#ACA VA EL READ DEL CSV
x_test=pd.read_csv('x_test.csv')
sub=x_test.iloc[:50,:]

def arreglarXML(df):
    df=df.replace(' ','_',regex=True)
    df=df.replace('-','_',regex=True)
    df=df.replace({'\(': '_', '\)': '_'}, regex=True)
    df=df.replace('__','_',regex=True)
    df=df.replace('>','_',regex=True)
    df=df.replace('<','_',regex=True)
    df=df.replace('/','_',regex=True)
    df=df.replace('\+', '_', regex=True)
    suplante=df.astype(str)
    suplante=df.applymap(str)
    df=suplante
    return df
def hallarProbabilidad(df):
    df=arreglarXML(df)
    probs=modelo.predict_probability(df)
    probs1=probs['Respuesta_1']
    threshold=0.20
    probs['resML']=(probs1>threshold).astype(int)
    masde360=sum(probs['resML'])
    ids=probs[probs['resML']==1].index.values
    cantidad=len(df)
    if masde360==0:
        return (f"de {cantidad} estudiantes suministrados, no se espera que alguno pueda ser postulado para la beca.")
    elif masde360==1:
        return(f"De {cantidad} estudiantes suministrados, solo se espera que 1 se pueda postular a la beca, que es el estuidante con id {ids}. ")
    else:
        return (f"De {cantidad} estudiantes suministrados, la cantidad esperada de estudiantes que pueden postularse a la beca son: {masde360}, los cuales tienen estos ids: {ids}. ")



######################
#    INICIO     TAB 1
######################
#df0 = pd.read_excel('D:/UNIANDES/ACTD/Git/Repositorio3/ACTD_Proyecto_3/datos8.xlsx',dtype={"cole_cod_mcpio_ubicacion": str,"cole_cod_mcpio_ubicacion":str})
# Se arreglan diferencias entre el df y el json
engine = psycopg2.connect(
    dbname="data8",
    user="postgres",
    password="contra123",
    host="carlos.cqghz6mj7lj8.us-east-1.rds.amazonaws.com",
    port='5432'
)
cursor = engine.cursor()
query = """
SELECT *
FROM datos8;"""
cursor.execute(query)
result = cursor.fetchall()
df0 = pd.DataFrame(result)



df0.columns = ['cole_depto_ubicacion','periodo','average_column','Anio','Prueba']


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

#df1 = pd.read_excel('D:/UNIANDES/ACTD/Git/Repositorio3/ACTD_Proyecto_3/opciones.xlsx')
#df2 = pd.read_excel('D:/UNIANDES/ACTD/Git/Repositorio3/ACTD_Proyecto_3/datosGra2.xlsx')
engine = psycopg2.connect(
    dbname="data8",
    user="postgres",
    password="contra123",
    host="carlos.cqghz6mj7lj8.us-east-1.rds.amazonaws.com",
    port='5432'
)
cursor = engine.cursor()
query = """
SELECT *
FROM datosGra2;"""
cursor.execute(query)
result = cursor.fetchall()
df2 = pd.DataFrame(result)
df2.columns = ['tipo documento','Población','Bilingue','Grado','Dpto Colegio','Región','Colegio genero','Colegio jornada','Colegio naturaleza','Nacimiento estudiante','Estudiante Genero','Num Cuartos','Educación Madre','Educación Padre','Estrato','Personas hogar','Tiene automovil','Tiene computador','Tiene internet','Tiene lavadora','Nota ingles','Candidato','ID']


df2= df2.value_counts(["Tiene computador","Tiene internet","Candidato"]).reset_index().rename(columns={0:"Conteo"})
fig2 = px.bar(df2, y="Conteo", x= "Candidato", color="Tiene computador", barmode="group",facet_row="Tiene internet", text_auto=True)#

opciones = []
#columnas = df1.shape[1]
#for num in range(1, columnas):
#    la_lista=df1.iloc[:,num].dropna().unique()
#    opciones.append(la_lista)

#print(opciones)

app = Dash(__name__)

app._favicon = ('favicon.ico') #must be in /assets/favicon.ico 
app.title = "PROYECTO 3 ACTD"

app.layout = html.Div([    

    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Nuestro País', value='tab-1', children=[
            
            dbc.Col([
                 
                 html.Br(),
                dbc.Row(html.Div("PUNTAJE PROMEDIO EN PRUEBAS SABER 11 POR DEPARTAMENTO", style={'fontSize': '24px', 'text-align':'center'})),
                dbc.Row(dcc.Graph(id='graph-with-slider',figure=fig)),
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
        
        dcc.Tab(label='Los estudiantes', value='tab-2', children=[  

             dcc.Graph(id='graph2',figure=fig2),      
        ]),

        dcc.Tab(label='Hallazgos', value='tab-3', children=[
             

             dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Arrastre o ',
                    html.A('seleccione el archivo')
        ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),

    html.Br(),
    dbc.Row(html.Div(id='output-data-upload2', style={'fontSize': '24px', 'text-align':'center'})),

            # dbc.Row([
            #     dbc.Col(
            #         html.Div(["¿Cuál es su región'",dcc.Dropdown(id='dropdownAge',options=opciones[0]),]),width=4), #,persistence=True, persistence_type='session'
            #     dbc.Col(
            #         html.Div(["¿En qué área se ubica el colegio?",dcc.Dropdown(id='dropdownSex',options=opciones[1],value='',),]),width=4),
            #     dbc.Col(
            #         html.Div(["¿Es el colegio bilingüe?",dcc.Dropdown(id='dropdownCPT',options=opciones[2],value='',),]),width=4),        
            #     dbc.Col(
            #         html.Div(["¿En qué departamento se ubica su colegio?",dcc.Dropdown(id='dropdownAge2',options=opciones[3]),]),width=4), #,persistence=True, persistence_type='session'
            #     dbc.Col(
            #         html.Div(["¿Cuál es el sexo biológico?",dcc.Dropdown(id='dropdownSex3',options=opciones[4],value='',),]),width=4),
            #     dbc.Col(
            #         html.Div(["¿Qué tipo de dolor de pecho?",dcc.Dropdown(id='dropdownCPT4',options=opciones[5],value='',),]),width=4), 
            # ]),

                        
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

       # dcc.Tab(label='Quienes somos', value='tab-4', children=[

            

       #     ]),    
          

        dcc.Tab(label='Estadisticas para Nerds', value='tab-4', children=[
            # Definimos las tablas
            # table1 = dash_table.DataTable(
            #     id='tabla1',
            #     columns=[{"name": i, "id": i} for i in df3.columns],style_cell={'textAlign': 'left'},
            #     data=df3.to_dict('records')
            # )

            # table2 = dash_table.DataTable(
            #     id='tabla2',
            #     columns=[{"name": i, "id": i} for i in df4.columns],style_cell={'textAlign': 'left'},
            #     data=df4.to_dict('records')
            # )

            #dcc.Tab(label='Evaluación del modelo', value='tab-1', children= table1),
            #dcc.Tab(label='Desempeño', value='tab-2', children= table2),
            ]    
                 ),
    ]),



    
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
    app.run_server(host = "0.0.0.0",debug=True)

