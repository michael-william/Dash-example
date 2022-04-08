import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Variable for sorting months
month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


# Getting dictionary for top colors
def top_colors(top5_sales_list,top5_units_list,top_ten_rgba):
    all_items = top5_sales_list
    all_items2 = [i for i in top5_units_list if i not in top5_sales_list]
    all_items3 = all_items+all_items2
    length = len(all_items3)
    top_colors_dict = dict(zip(all_items3,top_ten_rgba[:length]))
    return top_colors_dict

# ---------------- Card1-----------------------
#Getting raw number of total sold
def sales_total_func(dataset):
    return np.sum(dataset["Quantity"] * dataset["UnitPrice"])

#Turning raw number into human format
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

#Getting total sales for each month
def monthly_sales_func(dataset,order):
    monthly_sales_df = np.ceil(pd.DataFrame(dataset.groupby("Month")["Line totals"].sum())).loc[order]
    monthly_sales_df['labels'] = monthly_sales_df['Line totals'].apply(lambda x: '$'+human_format(x))
    return monthly_sales_df

#Plotting monthly_totals
def monthly_sales_plot_func(monthly_sales_df,line_color):
    monthly_sales_plot = go.Figure()
    monthly_sales_plot.add_trace(go.Scatter(x=monthly_sales_df.index, 
                                            y=monthly_sales_df['Line totals'], 
                                            mode='lines+markers',
                                            marker={"size":6},
                                            line_shape='spline',
                                            text=monthly_sales_df['labels'],
                                            hovertemplate = '%{x} %{text} <extra></extra>',
                                            line=dict(color=line_color),
                                            connectgaps=True))


    monthly_sales_plot.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                #family='Arial',
                size=12,
                #color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=True,
        #width=200,
        height=150,
        margin=dict(
            autoexpand=False,
            l=0,
            r=0,
            t=0,
            b=38,
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return monthly_sales_plot



#----------------- Card2 -------------------------
# Getting top 5 sales items
def top5_sales_func(dataset):
    desc_sales = pd.DataFrame(zip(dataset['Line totals'], dataset["Description"]))
    desc_sales.columns = ["Line totals","Item"]
    desc_sales_df = np.ceil(pd.DataFrame(desc_sales.groupby("Item")["Line totals"].sum())).sort_values('Line totals',ascending=False)
    desc_sales_df['labels'] = desc_sales_df['Line totals'].apply(lambda x: '$'+human_format(x))
    desc_sales_df = desc_sales_df.head()
    return desc_sales_df,list(desc_sales_df.index)

# Plotting top 5 sales items
def top5_sales_plot(top5_sales_df,color_dict):
    desc_sales_plot = go.Figure()

    for i in top5_sales_df.index:
        desc_sales_plot.add_trace(go.Scatter(y=[i,i], 
                                            x=[0,top5_sales_df.loc[i]['Line totals']], 
                                            mode='lines+markers',
                                            marker={"size":9},
                                            text = [top5_sales_df.loc[i]['labels']]*2,
                                            line=dict(color = color_dict[i],width=9),
                                            hovertemplate = '%{y} <br>%{text}<extra></extra>',
                                            #hoverinfo='skip',
                                            ))
        desc_sales_plot.add_annotation(xanchor='left',
                                x=0,
                                y=i,
                                text=i,
                                yshift=10,
                                xshift=-5,
                                font={'size':9},
                                showarrow=False,
                            )

    desc_sales_plot.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                #color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            autorange='reversed',
            showgrid=False,
            showline=False,
            showticklabels=False,
            tickangle=-45,
            tickfont=dict(
                family='Arial',
                size=9,
                #color='rgb(82, 82, 82)',
            )
        ),
        xaxis_tickprefix = '$',
        autosize=True,
        #width=200,
        height=200,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            autoexpand=False,
            l=0,
            r=0,
            t=0,
            b=35,
        ),
    )
    
    return desc_sales_plot



# -------------------- Card 5 ---------------------------
# Getting monthly sales trend for top 5 items
def top5_sales_monthly_func(dataset,top_list,order):
    desc_sales_trend = dataset.groupby(['Month',"Description"])['Line totals'].sum().reset_index()
    desc_sales_trend = pd.pivot(data = desc_sales_trend,index='Month', columns='Description', values='Line totals')
    desc_sales_trend = (desc_sales_trend[top_list]).replace(np.nan, 0).loc[order]
    return desc_sales_trend

# Plotting top 5 monthly sales trend

def top5_sales_monthly_plot(dataset,color_dict):
    top5_sales_plot = go.Figure()
    for item in dataset.columns:
        top5_sales_plot.add_trace(go.Scatter(
                                            x=dataset.index, 
                                            y=dataset[item], 
                                            mode='lines+markers',
                                            name=item,
                                            marker={"size":6},
                                            line_shape='spline',
                                            text=[item +': $' + human_format(x) for x in dataset[item]],
                                            hovertemplate = '%{text} <extra></extra>',
                                            line=dict(color= color_dict[item]),
                                            connectgaps=True)
                                )
    top5_sales_plot.update_layout(
        height=275,
        yaxis_tickprefix = '$',
        xaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            #ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            #showline=True,
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=9,
                color='rgb(82, 82, 82)',),
            tickangle=-45
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=20,
            r=0,
            t=0,
        ),
        showlegend=True,
        legend_title_side='left',
        legend_orientation='h',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return top5_sales_plot


# ---------------------Card 3 ------------------------
#Getting raw number of total units
def units_total_func(dataset):
    return np.sum(dataset["Quantity"])

#Getting total units for each month
def monthly_units_func(dataset,order):
    monthly_units_df = np.ceil(pd.DataFrame(dataset.groupby("Month")["Quantity"].sum())).loc[order]
    monthly_units_df['labels'] = monthly_units_df['Quantity'].apply(lambda x: human_format(x))
    return monthly_units_df

#Plotting monthly_units
def monthly_units_plot_func(monthly_units_df,line_color):
    monthly_units_plot = go.Figure()
    monthly_units_plot.add_trace(go.Scatter(x=monthly_units_df.index, 
                                            y=monthly_units_df['Quantity'], 
                                            mode='lines+markers',
                                            marker={"size":6},
                                            line_shape='spline',
                                            text=monthly_units_df['labels'],
                                            hovertemplate = '%{x} %{text} <extra></extra>',
                                            line=dict(color=line_color),
                                            connectgaps=True))


    monthly_units_plot.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                #family='Arial',
                size=12,
                #color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=True,
        #width=200,
        height=150,
        margin=dict(
            autoexpand=False,
            l=0,
            r=0,
            t=0,
            b=38,
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return monthly_units_plot


# ------------------ Card 4 ---------------------
# Getting top 5 units items
def top5_units_func(dataset):
    desc_units = pd.DataFrame(zip(dataset['Quantity'], dataset["Description"]))
    desc_units.columns = ["Quantity","Item"]
    desc_units_df = np.ceil(pd.DataFrame(desc_units.groupby("Item")["Quantity"].sum())).sort_values('Quantity',ascending=False)
    desc_units_df['labels'] = desc_units_df['Quantity'].apply(lambda x: human_format(x))
    desc_units_df = desc_units_df.head()
    return desc_units_df,list(desc_units_df.index)

# Plotting top 5 units items
def top5_units_plot(top5_units_df,color_dict):
    desc_units_plot = go.Figure()

    for ind,i in enumerate(top5_units_df.index):
        desc_units_plot.add_trace(go.Scatter(y=[i,i], 
                                            x=[0,top5_units_df.loc[i]['Quantity']], 
                                            mode='lines+markers',
                                            marker={"size":9},
                                            text = [top5_units_df.loc[i]['labels']]*2,
                                            line=dict(color = color_dict[i],width=9),
                                            hovertemplate = '%{y} <br>%{text}<extra></extra>',
                                            #hoverinfo='skip',
                                            ))
        desc_units_plot.add_annotation(xanchor='left',
                                x=0,
                                y=i,
                                text=i,
                                yshift=10,
                                xshift=-5,
                                font={'size':9},
                                showarrow=False,
                            )

    desc_units_plot.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                #color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            autorange='reversed',
            showgrid=False,
            showline=False,
            showticklabels=False,
            tickangle=-45,
            tickfont=dict(
                family='Arial',
                size=9,
                #color='rgb(82, 82, 82)',
            )
        ),
        #xaxis_tickprefix = '$',
        autosize=True,
        #width=200,
        height=200,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            autoexpand=False,
            l=0,
            r=0,
            t=0,
            b=35,
        ),
    )
    
    return desc_units_plot


# ------------------ Card 6 -----------------------
# Getting monthly units trend for top 5 items
def top5_units_monthly_func(dataset,top_list,order):
    desc_units_trend = dataset.groupby(['Month',"Description"])['Quantity'].sum().reset_index()
    desc_units_trend = pd.pivot(data = desc_units_trend,index='Month', columns='Description', values='Quantity')
    desc_units_trend = (desc_units_trend[top_list]).replace(np.nan, 0).loc[order]
    return desc_units_trend

# Plotting top 5 monthly units trend

def top5_units_monthly_plot(dataset,color_dict):
    top5_units_plot = go.Figure()
    for item in dataset.columns:
        top5_units_plot.add_trace(go.Scatter(
                                            x=dataset.index, 
                                            y=dataset[item], 
                                            mode='lines+markers',
                                            name=item,
                                            marker={"size":6},
                                            line_shape='spline',
                                            text=[item +': '+human_format(x) for x in dataset[item]],
                                            hovertemplate = '%{text} <extra></extra>',
                                            line=dict(color=color_dict[item]),
                                            connectgaps=True)
                                )
    top5_units_plot.update_layout(
        height=275,
        #yaxis_tickprefix = '$',
        xaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            #ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                #color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            #showline=True,
            showticklabels=True,
            tickangle=-45,
            tickfont=dict(
                family='Arial',
                size=9,
                #color='rgb(82, 82, 82)'
            )
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=20,
            r=0,
            t=0,
        ),
        showlegend=True,
        legend_title_side='left',
        legend_orientation='h',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
    return top5_units_plot