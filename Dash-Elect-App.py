#This works great!!!

import pandas as pd
import datetime as dt
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

colors = {'background': '#008B8B','text': '#FFF8DC'}

#Incorporate Data
df = pd.read_csv("https://raw.githubusercontent.com/BGQM/fpl/main/FPL_Bills.csv")
df['Date'] = pd.to_datetime(df['Date']) #Note: this is required to make into a datetime object
df = df.set_index('Date')
df['Month'] = df.index.month_name()
df['Year'] = df.index.year
year_list = sorted(df['Year'].unique())#Note: sorting is probably not necessary
max_year = df['Year'].max()

#Initialize app
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Avalon Electricity Usage and Cost',
                         style={'fontSize':28, 
                         'fontWeight' : 'bold',
                         'textAlign':'center', 
                         'color' : colors['text'],
                         'background-color' : colors['background']}),
    html.Hr(),#puts in a line
    dcc.RadioItems(id='selected_year', options=year_list, value=max_year, inline=True),
    html.Hr(),
    html.Button('Select kWh/Cost', n_clicks=0, id='button'),
    dcc.Graph(id="graph"),
    html.Hr(),
    #html.H1('Indicator gauges here...')
    #dcc.Markdown(id='text_displayed')
])

#Initial populate chart
@app.callback(
    Output("graph", "figure"), 
    Input("selected_year", "value"),
    Input("button", "n_clicks")
    )

def display_graph(value,n_clicks):
    df2 = df.loc[str(value)]
    if n_clicks % 2 == 0:
        x, y = df2['Month'], df2['kWh']
    else:
        x, y = df2['Month'], df2['Total']

    fig = px.bar(df2, x=x, y=y, text_auto=True, title=str(value) + " Avalon Monthly Electricity Usage/Cost") 
    #print(value)#this is just for monitoring
    #print(n_clicks)#this is just for monitoring
    #print(df2)   
    return fig

#Run app
if __name__ == '__main__':
    app.run(debug=True)
