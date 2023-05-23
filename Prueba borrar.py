import pandas as pd
import plotly.graph_objs as go
import json
from urllib.request import urlopen

"""## Importar json con las ubicaciones por departamento"""
with urlopen('https://raw.githubusercontent.com/finiterank/mapa-colombia-js/9ae3e4e6125e2589cc1ac8bf685ebb319d99cf08/colombia-municipios.json') as response:
    counties = json.load(response)
# Ojo el link al repositorio con el json falla luego de un tiempo, creo que no estoy generando bien el perma link
df = pd.read_csv('datos4.csv', delimiter=',')



locs = df['cole_mcpio_ubicacion']

for loc in counties['arcs']:
    loc['id'] = loc['properties']['name']

