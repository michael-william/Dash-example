from ctypes import alignment
from tkinter import font
from tkinter.ttk import Style
from turtle import color, width
import dash
import dash_bootstrap_components as dbc
#import dash_core_components as dcc
from dash import dcc
from dash import html
#from dash_html_components import Label
from folium import Div
#from matplotlib import colors
import plotly.graph_objects as go
import numpy as np
from numpy import size
from pandas.io.formats import style
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from sqlalchemy import column
from sympy import carmichael

import transformations as tr

#Formats
pink_hex = '#d63384'
pink_rgba = 'rgba(214, 51, 132,1)'
top5_colors = ['rgba(214, 51, 132,1)', 'rgba(242, 117, 181, 1)',
                'rgba(246, 137, 193, 1)', 'rgba(253, 167, 211, 1)',
                'rgba(255, 183, 220, 1)']

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


# Importing data
df = pd.read_csv('/Users/michaelcondon/Documents/DataAndStories/Codebase/Dash-template/data/Condensed data from online retail.csv',
                parse_dates=["InvoiceDay"])
months = df["InvoiceDay"].dt.strftime('%b')
years = df["InvoiceDay"].dt.strftime('%Y')
df["Month"] = months
df["Year"] = years
df['Line totals'] = df['Quantity'] * df['UnitPrice']

# Filtered datasets by orders and refunds
# Only using orders from here on out
ordered = df[(df['TransType']=='Ordered') & (df['Year']=='2020')].copy().reset_index()
#refunds = df[(df['TransType']!='Ordered') & (df['Year']=='2020')].copy().reset_index()

#Card 1 (Sales total and trend)
sales_total = tr.sales_total_func(ordered)
total_sold_short = tr.human_format(sales_total)
monthly_sales_df = tr.monthly_sales_func(ordered, tr.month_order)

#Card 2 (Top 5 sales items)
top5_sales,top5_sales_list = tr.top5_sales_func(ordered)

#Card 5 (Top 5 monthly sales items)
top5_sales_monthly = tr.top5_sales_monthly_func(ordered,top5_sales_list)

# Card 3 (Units sold number)
units_total = tr.units_total_func(ordered)
units_total_short = tr.human_format(units_total)
monthly_units_df = tr.monthly_units_func(ordered, tr.month_order)
 
#Card 4 (Top 5 its by units)
top5_units,top5_units_list = tr.top5_units_func(ordered)

#Card 6
top5_units_monthly = tr.top5_units_monthly_func(ordered,top5_units_list)

#Colors
top_color_dict = tr.top_colors(top5_sales_list, top5_units_list, top_ten_light)

#Graphs
monthly_sales_graph = tr.monthly_sales_plot_func(monthly_sales_df,pink_hex)
top5_sales_graph = tr.top5_sales_plot(top5_sales,top_color_dict)
top5_sales_monthly_graph = tr.top5_sales_monthly_plot(top5_sales_monthly, top_color_dict)
monthly_units_graph = tr.monthly_units_plot_func(monthly_units_df, pink_rgba)
top5_units_graph = tr.top5_units_plot(top5_units,top_color_dict)
top5_units_monthly_graph = tr.top5_units_monthly_plot(top5_units_monthly, top_color_dict)

# defining the app
app = dash.Dash(
    __name__,
    external_stylesheets=["/Users/michaelcondon/Documents/DataAndStories/Codebase/Dash-template/assets/bootstrap.css"]
)

# App layout
app.layout = html.Div(
    [
        html.Div(
            className="container",
            children=[
        dbc.Row([
            dbc.Col(children=[
                html.H1("Product perfomance"),
                html.H3("Top products & trends")
                ]),
            dbc.Col([
                
                
                dcc.RangeSlider(
                            id='month_slider',
                            min=1,
                            max=12,
                            step=1,
                            value=[1,12],
                            allowCross=False,
                            marks={
                                1: 'Jan',
                                2: 'Feb',
                                3: 'Mar',
                                4: 'April',
                                5: 'May',
                                6: 'Jun',
                                7: 'Jul',
                                8: 'Aug',
                                9: 'Sep',
                                10: 'Oct',
                                11: 'Nov',
                                12: 'Dec'
                            },

                            className="rc-slider",
                        ),
                        ],
                        width=4,
                        style={'position': 'absolute',
                        'bottom':30,
                        'right':0,
                                    }    
                )
            ],
            style={'position': 'relative'
                                    }
            ),
        dbc.Row(
            [
                dbc.Col([
                    html.H6("Revenue this year"),
                    html.H4("$"+total_sold_short),
                    dcc.Graph(
                        id='total-sales',
                        figure=monthly_sales_graph,
                        config={'displayModeBar': False}
                        )
                ],
                className="raised-container",
                style={'width':'23%'},
                width=3
                ),
                dbc.Col([
                    html.H6("Top 5 sales items"),
                    dcc.Graph(
                        figure=top5_sales_graph,
                        config={'displayModeBar': False}
                        )],
                className="raised-container",
                style={'width':'23%'},
                width=3,
                ),
                dbc.Col([
                    html.H6("Items sold this year"),
                    html.H4(units_total_short),
                    dcc.Graph(
                        figure=monthly_units_graph,
                        config={'displayModeBar': False}
                        )],
                className="raised-container",
                style={'width':'23%'},
                width=3
                ),
                dbc.Col([
                    html.H6("Top 5 items sold"),
                    dcc.Graph(
                        figure=top5_units_graph,
                        config={'displayModeBar': False}
                        )],
                className="raised-container",
                style={'width':'23%'},
                width=3,
                ),
            ],
            style={'margin-top':'15px', 'row-gap':"10px"}
        ),
        dbc.Row(
            [
                dbc.Col([
                    html.H6("Top 5 sales trend"),
                    dcc.Graph(
                        figure=top5_sales_monthly_graph,
                        config={'displayModeBar': False}
                        )
                    ],
                className="raised-container",
                ),
                dbc.Col([
                    html.H6("Top 5 sold items"),
                    dcc.Graph(
                        figure=top5_units_monthly_graph,
                        config={'displayModeBar': False}
                        )
                    ],
                className="raised-container",
                ),
            ],
            style={'margin-top':'10px'}
        ),
        ]
        )
    ]
)

# Initializing the app
if __name__ == "__main__":
    app.run_server(debug=True)