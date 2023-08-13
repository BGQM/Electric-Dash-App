import pandas as pd
import datetime as dt
import dash
from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

colors = {'background': '#0086b3','text': '#ffffff'}#blue background and white text - Note: This matches the YETI theme!

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server

### Data =======================================================================================

df = pd.read_csv("https://raw.githubusercontent.com/BGQM/fpl/main/FPL_Bills.csv")
df['InvoiceDate'] = df['Date']#Create column for Dash AG grid
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
df['Month'] = df.index.month_name()
df['Year'] = df.index.year
df['UnitRate'] = round(df['Total']/df['kWh'],3)#Add column for unit rate
year_list = sorted(df['Year'].unique())
max_year = df['Year'].max()

### Column Definitions for Dash AG Grid =========================================================

columnDefs = [
    { 'field': 'InvoiceDate', 'headerName': 'Invoice Date', 'filter':False },
    { 'field': 'kWh', 'headerName': 'Consumption (kWh)'},
    { 'field': 'Total', 'headerName': 'Total ($)', 'valueFormatter': {'function': "d3.format('$,.2f')(params.value)"}},
    { 'field': 'UnitRate', 'headerName': 'Unit Rate ($/kWh)', 'valueFormatter':{'function': "d3.format('$,.3f')(params.value)"}}
]

### Tab Style Information =======================================================================

tabs_styles = {
    'height': '36px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'normal',
    'border-radius': '6px'
}    

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': colors['background'],
    'fontWeight': 'normal',
    'color': 'white',
    'border-radius': '6px',
    'padding': '6px'
}

### Dash AG Grid =====================================================================================

grid = dag.AgGrid(
    id='grid-1',
    className='ag-theme-alpine',
    columnDefs=columnDefs,
    columnSize='sizeToFit',
    rowData=df.to_dict('records'),   
    #dashGridOptions={'pagination':True, 'paginationPageSize':10},#this works when you need to limit the rows on each page
    dashGridOptions={'pagination':True},
    csvExportParams={'fileName': 'fpl_data.csv'},
    #dashGridOptions={"pinnedBottomRowData": [{}]}
)

### Bootstrap Card ======================================================================================

card1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5('Total Consumption', className='card-title', style={'fontWeight' : 'bold','textAlign':'center'})
            ]
        ),
        dbc.CardFooter(id='consumption', style={'fontSize':28, 'fontWeight' : 'bold','textAlign':'center'}),
    ],
    style={'width': '18rem'},
)

card2 = dbc.Card([  
        dbc.CardBody(
            [
                html.H5('Total Cost', className='card-title', style={'fontWeight' : 'bold','textAlign':'center'}),
            ]
        ),
        dbc.CardFooter(id='cost', style={'fontSize':28,'fontWeight' : 'bold','textAlign':'center'}),
    ],
    style={'width': '18rem'},
)

card3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5('Average Unit Cost', className='card-title',style={'fontWeight' : 'bold','textAlign':'center'}),
            ]
        ),
        dbc.CardFooter(id='unitcost', style={'fontSize':28,'fontWeight' : 'bold','textAlign':'center'}),
    ],
    style={'width': '18rem'},
)

app.layout = dbc.Container([
    dbc.Row([
       dbc.Col([
           html.H1("Avalon Electricity Usage",
           style={'fontSize':24, 
                'fontWeight' : 'bold',
                'textAlign':'center', 
                'color' : colors['text'],
                'background-color' : colors['background']
                 }),
            html.Hr(),
            dbc.RadioItems(id='selected_year', options=year_list, value=max_year, inline=True, 
            labelStyle={'display':'inline-block','margin-right': '15px'}),
            html.Hr(),
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Annual Summary', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Monthly Consumption', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Monthly Cost', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Monthly Unit Rate', value='tab-4', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Monthly Distribution', value='tab-5', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Unit Rate Trend', value='tab-6', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Data Table', value='tab-7', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
            html.Div(id='tabs-content-inline')
       ], width=12)
    ], justify="center"),
])

# Callback and function to display tabs
@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Hr(),
            dbc.Row([
            dbc.Col(
                html.H2(id='graph91_title', className='text-center',style={'fontWeight':'bold'})),
                html.Hr(),
            ]),
            dbc.Row([
                dbc.Col(card1, width=4),
                dbc.Col(card2, width=4),
                dbc.Col(card3, width=4)
                ])
            ]) 
    elif tab == 'tab-2':
        return html.Div([
            html.Hr(),
            html.H3(id='graph92_title', style={'fontWeight':'bold','textAlign':'center'}),
            dcc.Graph(id="graph92")
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Hr(),
            html.H3(id='graph93_title', style={'fontWeight' : 'bold','textAlign':'center'}),
            dcc.Graph(id="graph93")
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.Hr(),
            html.H3(id='graph94_title', style={'fontWeight':'bold','textAlign':'center'}),
            dcc.Graph(id="graph94")
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.Hr(),
            html.H3(id='graph95_title', style={'fontWeight':'bold','textAlign':'center'}),
            dcc.Graph(id="graph95")
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.Hr(),
            html.H3(id='graph96_title', style={'fontWeight':'bold','textAlign':'center'}),
            dcc.Graph(id="graph96")
        ])
    elif tab == 'tab-7':
        return html.Div([
            html.Hr(),
            html.H3(id='graph97_title', style={'fontWeight':'bold','textAlign':'center'}),
            grid,
            html.H5('Download complete dataset', style={'fontWeight':'bold'}),
            dbc.Button('Download CSV', id='csv-button', n_clicks=0, style={'border-radius': '6px'})  
        ])
    
                      
# Callback and function for year selected
@app.callback(
    Output('my-output', 'children'),
    Input('selected_year', 'value')
)
def update_output_div(input_value):
    return f'{input_value}'


#Callback and function for Annual Summary
@app.callback(
    Output('graph91_title', 'children'),
    Output('consumption', 'children'),
    Output('cost', 'children'),
    Output('unitcost', 'children'),
    Input('selected_year', 'value')
)
def display_graph(value):
    dff = df.loc[str(value)]
    graph91_title = str(value) + '  Summary'
    total_kWh = str((f"{(dff['kWh'].sum()):,.0f}")) + ' kWh'
    total_cost = '$' + str((f"{(dff['Total'].sum()):,.2f}"))
    unit_cost = '$' + str((f"{(dff['Total'].sum()/dff['kWh'].sum()):,.3f}")) + ' per kWh'
    return graph91_title, total_kWh, total_cost, unit_cost


# Callback and function for monthly kWh consumption
@app.callback(
    Output("graph92", "figure"),
    Output('graph92_title', 'children'),
    Input('selected_year', 'value')
)
def display_graph(value):
    dff = df.loc[str(value)]
    x, y = dff['Month'], dff['kWh']
    graph92_title = str(value) + '  Monthly kWh Consumption'
    fig = px.bar(dff, x=x, y=y, text_auto=True
    )  
    return fig,graph92_title


# Callback and function for monthly cost
@app.callback(
    Output("graph93", "figure"),
    Output('graph93_title', 'children'),
    Input('selected_year', 'value')
)
def display_graph(value):
    dff = df.loc[str(value)]
    x, y = dff['Month'], dff['Total']
    graph93_title = str(value) + '  Monthly Cost($)'
    fig = px.bar(dff, x=x, y=y, text_auto=True
    )  
    return fig,graph93_title


# Callback and function for monthly unit rate
@app.callback(
    Output("graph94", "figure"),
    Output('graph94_title', 'children'),
    Input('selected_year', 'value')
)
def display_graph(value):
    dff = df.loc[str(value)]
    x, y = dff['Month'], round(dff['Total']/dff['kWh'],3)
    graph94_title = str(value) + '  Monthly Unit Rate ($/kWh)'
    fig = px.bar(dff, x=x, y=y, labels={'y':'$/kWh'},text_auto=True
    )  
    return fig,graph94_title


# Callback and function for monthly distribution pie chart
@app.callback(
    Output("graph95", "figure"),
    Output('graph95_title', 'children'),
    Input('selected_year', 'value')
)
def display_graph(value):
    dff = df.loc[str(value)]
    graph95_title = str(value) + '  Monthly kWh Distribution'
    fig = px.pie(dff, values='kWh', names='Month'
    )
    return fig,graph95_title


# Callback and function for unit rate trend
@app.callback(
    Output("graph96", "figure"),
    Output('graph96_title', 'children'),
    Input('selected_year', 'value')
)
def display_graph(value):
    df['UnitRate'] = df['Total']/df['kWh']
    dff = df
    x, y = dff['Year'], dff['UnitRate']
    graph96_title = 'Unit Rate Trend ($/kWh)'
    fig = px.line(dff, x=x, y=y, color = 'Month', labels={'y':'$/kWh'}, markers=True
    )  
    return fig,graph96_title


# Callback and function for data grid
@app.callback(
    Output('grid-1', 'exportDataAsCsv'),
    Input('csv-button', 'n_clicks'),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False

### Run App ======================================================

if __name__ == "__main__":
    app.run(debug=False)
