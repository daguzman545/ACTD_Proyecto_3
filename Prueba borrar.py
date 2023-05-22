import pandas as pd
import plotly.graph_objs as go
import json
from urllib.request import urlopen

"""## Importar json con las ubicaciones por departamento"""
with urlopen('https://github.com/finiterank/mapa-colombia-js/blob/9ae3e4e6125e2589cc1ac8bf685ebb319d99cf08/colombia-municipios.json') as response:
    counties = json.load(response)

df = pd.read_csv('datos2.csv', header=None, delimiter=',')

locs = df['cole_depto_ubicacion']

for loc in counties['Topology']:
    loc['id'] = loc['properties']['name']

