import plotly.graph_objects as go
import json
from urllib.request import urlopen
with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
    counties = json.load(response)

for loc in counties['objects']["depts"]["geometries"]:
    print(loc["properties"]["dpt"])  
fig = go.Figure(go.Choroplethmapbox(
                    geojson=counties,
                    locations=locs,
                    z=[1, 2, 3],
                    colorscale='Viridis',
                    colorbar_title="Thousands USD"))
fig.update_layout(mapbox_style="carto-positron",
                        mapbox_zoom=3,
                        mapbox_center = {"lat": 4.570868, "lon": -74.2973328})
fig.show()