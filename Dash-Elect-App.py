import pandas as pd
import datetime as dt
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
#from pandas_ods_reader import read_ods

colors = {'background': '#0086b3','text': '#ffffff'}#blue background and white text - Note: This matches the YETI theme!

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server

df = pd.read_csv("https://raw.githubusercontent.com/BGQM/fpl/main/FPL_Bills.csv")
#df = read_ods('/home/wg/Documents/WG Personal/FPL_Bills.ods')#this works, but only locally
df['Date'] = pd.to_datetime(df['Date']) #Note: this is required to make into a datetime object
df = df.set_index('Date')
df['Month'] = df.index.month_name()
df['Year'] = df.index.year
year_list = sorted(df['Year'].unique())#Note: sorting is probably not necessary
max_year = df['Year'].max()

app.layout = html.Div([
    dcc.Markdown('#### Avalon Electricity Usage',
            style={'fontSize':24, 
                    'fontWeight' : 'bold',
                    'textAlign':'center', 
                    'color' : colors['text'],
                    'background-color' : colors['background']
                    }),
    html.Hr(),
    
    dcc.RadioItems(id='selected_year', options=year_list, value=max_year, inline=True,
        labelStyle={'display':'inline-block','padding':'50','margin-left': '10px'}),
    html.Hr(),
    html.Button('Select kWh/Cost', n_clicks=0, id='button'),
    dcc.Graph(id="graph"),
    html.Hr(),
])

@app.callback(
    Output("graph", "figure"), 
    Input("selected_year", "value"),
    Input("button", "n_clicks")
    )

def display_graph(value,n_clicks):
    dff = df.loc[str(value)]
    avg_kWh = round(dff['Total'].sum()/dff['kWh'].sum(),3)
    if n_clicks % 2 == 0:
        x, y = dff['Month'], dff['kWh']
        chart_title = str(dff['kWh'].sum()) + " kWh"
    else:
        x, y = dff['Month'], dff['Total']
        chart_title = str(dff['Total'].sum()) + " ($)"
    fig = px.bar(dff, x=x, y=y, text_auto=True, title='Total Usage/Cost = ' + chart_title + "  --  Average Price: $/" + str(avg_kWh))  
    return fig

    #Run app
if __name__ == "__main__":
    app.run(debug=False)
