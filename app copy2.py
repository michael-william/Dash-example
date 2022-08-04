import os
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output

import transformations as tr

#Formats
pink_hex = '#d63384'
pink_rgba = 'rgba(214, 51, 132,1)'
top5_colors = ['rgba(214, 51, 132,1)', 'rgba(242, 117, 181, 1)',
                'rgba(246, 137, 193, 1)', 'rgba(253, 167, 211, 1)',
                'rgba(255, 183, 220, 1)']

"""
color_hex = {'blue': '#378dfc',
            'indigo': '#6610f2',
            'purple': '#5b62f4',
            'red': '#e52527',
            'orange': '#fd7e14',
            'yellow': '#ffc107',
            'green': '#43cc29',
            'teal': '#20c997',
            'cyan': '#0dcaf0',}


color_rgba ={'blue': 'rgba(55, 141, 252, 1)',
            'indigo': 'rgba(102, 16, 242, 1)',
            'purple': 'rgba(91, 98, 244, 1)',
            'red': 'rgba(229, 37, 39, 1)',
            'orange': 'rgba(253, 126, 20, 1)',
            'yellow': 'rgba(255, 193, 7, 1)',
            'green': 'rgba(67, 204, 41, 1)',
            'teal': 'rgba(32, 201, 151, 1)',
            'cyan': 'rgba(13, 202, 240, 1)'}


top_ten_rgba = ['rgba(102, 16, 242, 1)', #'indigo'
                'rgba(55, 141, 252, 1)', #'blue'
                'rgba(13, 202, 240, 1)', #'cyan'
                'rgba(32, 201, 151, 1)', #'teal'
                'rgba(230, 217, 30, 1)', #'yellow': 
                'rgba(253, 126, 20, 1)', #'orange'
                'rgba(255, 75, 75, 1)', # red
                'rgba(127, 138, 153, 1)', #'grey'
                'rgba(68, 75, 64, 1)', #'dark grey'
                'rgba(255, 255, 15, 1)' #'white' 
                ]
"""

top_ten_light = ['#dc83f2', #'indigo'
                '#83aef2', #'blue'
                '#83f2f0', #'cyan'
                '#83e6d5', #'teal'
                '#f0ea9c', #'yellow': 
                '#f0be62', #'orange'
                '#f09686', # red
                '#d9f5d4', #'green'
                '#949392', #'dark grey'
                '#ff0000' #'white' 
                ]

month_dict = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
    }

# Get the current working directory
cwd = os.getcwd()
# Add path for data
file_path = cwd+'/data/Condensed data from online retail.csv'

# Getting logo
logo = cwd+'/assets/dataandstories_logo 300.png'

# Importing data
df = pd.read_csv(file_path,
                parse_dates=["InvoiceDay"])
months = df["InvoiceDay"].dt.strftime('%b')
years = df["InvoiceDay"].dt.strftime('%Y')
df["Month"] = months
df["Year"] = years
df['Line totals'] = df['Quantity'] * df['UnitPrice']

# Filtered datasets by orders and refunds
# Only using orders from here on out
ordered = df[(df['TransType']=='Ordered') & (df['Year']=='2020')].copy().reset_index()

# defining the app
app = dash.Dash(
    __name__,
    meta_tags=[{'name': 'viewport',
    'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
    title="Product performance",
    external_stylesheets=[cwd+"/assets/bootstrap.css"]
)
server = app.server # Important! Nedded for hosting on Heroku

# App layout
app.layout = html.Div(
    [
        html.Div(
            className="container",
            children=[
        # Header
        dbc.Row([
            dbc.Col(children=[
                html.H1("Product perfomance"),
                html.H3("Top products & trends")
                ],
                # Columns widths for different size screens
                #xs=10, sm=8, md=5, lg=5, xl=5
                ),
            dbc.Col([
                html.A(
                    html.Img(
                        src=app.get_asset_url('ds_logo.png'),
                        alt='Dashboard built and designed by Michael at Data and Stories',
                        height='70px'
                    ),
                    href='https://www.dataandstories.com',
                    target="_blank",
                    style={'position': 'absolute',
                        'top':-65,
                        'right':30,},
                    ),
                dcc.RangeSlider(
                            id='month-slider',
                            min=1,
                            max=12,
                            step=1,
                            value=[1,12],
                            allowCross=False,
                            pushable=0,
                            marks=month_dict,
                            className="rc-slider",
                        ),
                        ],
                width=4,
                style={'position': 'absolute',
                'bottom':30,
                'right':0,
                'display': 'flex',
                    },
                #className="list-group-horizontal-md",
                #scaling columns for different size screens
                #xs=10, sm=8, md=5, lg=6, xl=5    
                )
            ],
            style={
                'position': 'fixed',
                'display': 'flex',
                'top':0,
                'left':0,
                'width':'101%',
                'padding-top':'1em',
                'background-color':'#fff',
                'z-index':'999',
                'box-shadow': '0px 10px 30px rgba(225,225,225,0.7)',
                'flex-direction':'row',
                
                                    },
                                    
            ),
        
        # Spacer row sits behind header
        dbc.Row([
        ],
        style={
            'height':'150px'
        }),
        
        # Rev cards
        dbc.Row([
                dbc.Row([
                    html.H2("Revenue"),
                ],
                ),
                dbc.Row([
                    dbc.Col([
                        html.P('Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.'),
                        html.Ul(children=[
                            html.Li('Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.'),
                            html.Li('Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.'),
                            html.Li('Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.'),
                            html.Li('Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.'),
                            html.Li('Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.'),
                            html.Li('Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.'),
                            ], id='insights-revenue', style={'width':'100%', 'height':'100%'}),
                    ],
                        #className="raised-container",
                        style={'width':'49%'},
                        width=6,
                    ),
                    dbc.Col([
                        dbc.Row([
                            html.H6("Total revenue"),
                            html.H4(
                            #"$"+total_sold_short,
                            id='total-sold-short',
                            ),
                            dcc.Graph(
                                id='monthly-sales-graph',
                                #figure=monthly_sales_graph,
                                config={'displayModeBar': False}
                                )
                            ],
                            className="raised-container",
                            style={'margin-bottom':'1em', 'display':'flex'},
                        ),
                        dbc.Row([
                            html.H6("Top 5 sales items"),
                            dcc.Graph(
                                id='top5-sales-graph',
                                #figure=top5_sales_graph,
                                config={'displayModeBar': False}
                            )
                        ],
                            className="raised-container",
                            style={'display':'flex'},
                            ),
                        
                    ],
                        style={'width':'49%'},
                        width=6,
                    ),
        ],)],
        style={'margin-top':'15px', 'row-gap':"10px"}
        ),

        
        # Item cards
        dbc.Row([
                dbc.Row([
                    html.H2("Items sold"),
                ],
                ),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            html.H6("Items sold this year"),
                            html.H4(
                                #units_total_short,
                                id='units-total-short',),
                            dcc.Graph(
                                id='monthly-units-graph',
                                #figure=monthly_units_graph,
                                config={'displayModeBar': False}
                                )],
                            className="raised-container",
                            style={'margin-bottom':'1em'}
                        ),
                        dbc.Row([
                            html.H6("Top 5 items sold"),
                            dcc.Graph(
                                id='top5-units-graph',
                                #figure=top5_units_graph,
                                config={'displayModeBar': False},
                                style={}
                                )],
                            className="raised-container",
                            ),
                        
                    ],
                        style={'width':'49%'},
                        width=6,
                    ),
                    dbc.Col([
                        html.P('Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.'),
                        html.Ul(children=[
                            html.Li('Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.'),
                            html.Li('Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.'),
                            html.Li('Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.'),
                            html.Li('Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.'),
                            html.Li('Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.'),
                            html.Li('Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.'),
                            ], id='insights-items', style={'width':'100%', 'height':'100%'}),
                    ],
                        #className="raised-container",
                        style={'width':'49%'},
                        width=6,
                    ),
        ],)],
        style={'margin-top':'35px', 'row-gap':"10px"}
        ),

       
        
        
        ]
        )
    ],
)

@app.callback(
    [
    Output(component_id="total-sold-short",component_property="children"),
    Output(component_id="monthly-sales-graph",component_property="figure"),
    Output(component_id="top5-sales-graph",component_property="figure"),
    Output(component_id="units-total-short",component_property="children"),
    Output(component_id="monthly-units-graph",component_property="figure"),
    Output(component_id="top5-units-graph",component_property="figure"),
    ],
    [Input(component_id="month-slider", component_property='value')]
)

def update_graphs(months):
    list_month_num = [i for i in range(months[0], (months[-1])+1)]
    list_month_name = [month_dict[i] for i in list_month_num]
    dff = ordered[ordered['Month'].isin(list_month_name)]

    #Card 1 (Sales total and trend)
    sales_total = tr.sales_total_func(dff)
    total_sold_short = tr.human_format(sales_total)
    monthly_sales_df = tr.monthly_sales_func(dff, list_month_name)

    #Card 2 (Top 5 sales items)
    top5_sales,top5_sales_list = tr.top5_sales_func(dff)

    #Card 5 (Top 5 monthly sales items)
    top5_sales_monthly = tr.top5_sales_monthly_func(dff,top5_sales_list, list_month_name)

    # Card 3 (Units sold number)
    units_total = tr.units_total_func(dff)
    units_total_short = tr.human_format(units_total)
    monthly_units_df = tr.monthly_units_func(dff, list_month_name)
    
    #Card 4 (Top 5 its by units)
    top5_units,top5_units_list = tr.top5_units_func(dff)

    #Card 6
    top5_units_monthly = tr.top5_units_monthly_func(dff,top5_units_list,list_month_name)

    #Colors
    top_color_dict = tr.top_colors(top5_sales_list, top5_units_list, top_ten_light)

    #Graphs
    monthly_sales_graph = tr.monthly_sales_plot_func(monthly_sales_df,pink_hex)
    top5_sales_graph = tr.top5_sales_plot(top5_sales,top_color_dict)
    top5_sales_monthly_graph = tr.top5_sales_monthly_plot(top5_sales_monthly, top_color_dict)
    monthly_units_graph = tr.monthly_units_plot_func(monthly_units_df, pink_rgba)
    top5_units_graph = tr.top5_units_plot(top5_units,top_color_dict)
    top5_units_monthly_graph = tr.top5_units_monthly_plot(top5_units_monthly, top_color_dict)

    return "$"+total_sold_short, monthly_sales_graph, top5_sales_graph, units_total_short, monthly_units_graph, top5_units_graph, 
    


# Initializing the app
if __name__ == "__main__":
    app.run_server(debug=True)
