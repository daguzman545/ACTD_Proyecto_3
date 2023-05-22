import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

#Initialise default settings

INIT_TITLE_TEXT = "PROYECTO 3 ACTD"
INIT_TITLE_H = "6vmin" # "7vh"
INIT_TITLE_DIV_H = "7vmin"
INIT_TITLE_PAD_TOP = "1vmin"
INIT_TITLE_COL = "white"                                 # title colour
INIT_TITLE_BG_COL = "grey"                               # title background
INIT_TITLE_OPACITY = 0.8                                 # title opacity
INIT_FONT_MASTER = ""
INIT_TITLE_FONT = INIT_FONT_MASTER
INIT_SELECTION_H = "2.3vmin" 

INIT_LOADER_TYPE = 'dot'
INIT_LOADER_DATASET_COLOR = "#3E3F3A"


    
"""Create a Plotly Dash dashboard."""
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP #FLATLY UNITED SANDSTONE PULSE
    ],
    #update_title=None          
)
server = app.server

# Create Dash Layout
app._favicon = ('favicon.ico') #must be in /assets/favicon.ico 
app.title = "WORLD ATLAS 2.0" #browser tab
#dash_app.index_string = dash_html.index_string


# Initialize callbacks after our app is loaded
#init_callbacks(dash_app)

 



  
create_dash_layout_button_group = dbc.ButtonGroup(
    [
        dbc.Button("First"),
        dbc.Button("Second"),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
            label="Dropdown",
            group=True,
        ),
    ]
)   

def create_dash_layout_header():
            
    #title of app in page
    title = html.Div([
        html.Span(INIT_TITLE_TEXT, style={"marginBottom": 0,
                                        #"marginTop": INIT_TITLE_PAD_TOP,
                                        #"marginLeft": 0,
                                        #'textAlign': 'center',
                                        'fontWeight': 'bold',
                                        'fontFamily': INIT_TITLE_FONT,
                                        'fontSize': INIT_TITLE_H,
                                        'height': INIT_TITLE_DIV_H,
                                        'color':INIT_TITLE_COL,
                                        'backgroundColor': INIT_TITLE_BG_COL,
                                        'opacity': INIT_TITLE_OPACITY}, 
        ),  
        ], style={"marginBottom": 0,
                                        "marginTop": INIT_TITLE_PAD_TOP,
                                        "marginLeft": 0,
                                        'textAlign': 'center',                                        
                                        'height': INIT_TITLE_DIV_H }, 
        )
   
    
    loader_main = html.Div(
                dcc.Loading(
                type=INIT_LOADER_TYPE,
                color=INIT_LOADER_DATASET_COLOR, #hex colour close match to nav bar ##515A5A
                children=html.Span("No data selected", id="my-loader-main", style={"marginBottom": 0, "marginTop": 10, "marginLeft": 0, 'textAlign': 'center', 'fontSize': INIT_SELECTION_H, 'fontFamily': 'Helvetica', 'fontWeight': '', 'backgroundColor': INIT_TITLE_BG_COL, 'opacity': INIT_TITLE_OPACITY  },), #style of span
                style={'textAlign': 'center' } #style of loader
                ),style={'textAlign': 'center', 'marginTop':10, 'marginBottom':10, 'color': INIT_TITLE_COL}, #style of div
    )
  
            
       
        
    #wrap the title, loader and selection up in a container called header
    header = dbc.Container([
        dbc.Row([
            dbc.Col([title, loader_main]),        
            ])            
        ],
        style={"marginBottom": 0,
               "marginTop": 0,
               "marginLeft": 0,
               "marginRight": 0,
               #"margin-left": "auto",
               #"margin-right": "auto",               
               #'backgroundColor':'white',
               "max-width": "none",
               "width": "100vw",
               "position": "absolute",
               "z-index": "2",
               #"top": "0vh",
               #"left": "5vw",
               }) 
            
    
    return header

def create_dash_layout_button_group():
    
    layout_button_group = dbc.ButtonGroup(
    [
        dbc.Button("Primero"),
        dbc.Button("Segundo"),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
            label="Tercero",
            group=True,
        ),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Item A"), dbc.DropdownMenuItem("Item B")],
            label="Cuarto",
            group=True,
        ),
    ]
    ) 
    return layout_button_group
#CONSTRUCT DASH LAYOUT

# Header
header = create_dash_layout_header()
button_group = create_dash_layout_button_group()
   
app.layout = html.Div([ button_group,header])

if __name__ == '__main__':
    app.run_server(debug=True)