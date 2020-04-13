import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df2 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# Bar chart data
barchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.sort_values(by=['Total'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['NOC'], y=barchart_df['Total'])]

# Stack bar chart data
stackbarchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stackbarchart_df = stackbarchart_df.sort_values(by=['Total'], ascending=[False]).head(20).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Gold'], name='Gold', marker={'color': 'gold'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Silver'], name='Silver', marker={'color': 'silver'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Bronze'], name='Bronze', marker={'color': '#CD7F32'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
line_df = df2
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=line_df['date'], y=line_df['actual_max_temp'], mode='lines', name='actual_max_temp')]

# Multi Line Chart
multiline_df = df2
multiline_df['date'] = pd.to_datetime(multiline_df['date'])
trace1_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_max_temp'], mode='lines', name='Max')
trace2_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_min_temp'], mode='lines', name='Min')
trace3_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_mean_temp'], mode='lines', name='Mean')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df2.groupby(['month']).agg(
    {'average_min_temp': 'max', 'average_max_temp': 'min'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['average_max_temp'],
               y=bubble_df['average_min_temp'],
               text=bubble_df['month'],
               mode='markers',
               marker=dict(size=bubble_df['average_max_temp'], color=bubble_df['average_max_temp'], showscale=True))
]

# Heatmap
data_heatmap = [go.Heatmap(x=df2['day'],
                           y=df2['month'],
                           z=df2['record_max_temp'].values.tolist(),
                           colorscale='Jet')]
# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Olympics 2016 and Weather 2014-2015', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number medals of Olympic 2016 of 20 first top Countries.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Number of Medals of Olympic 2016 of first 20 top Countries',
                                      xaxis={'title': 'Countries'}, yaxis={'title': 'Number of Medals'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represent the Gold, Silver, and Bronze Medal of Olympic of top 20 Countries'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Medals in the top 20 Countries',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Number of Medals'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the maximum temperature.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Actual Maximum Temperature from 2014 to 2015',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represent the maximum, minimum, and mean temperature.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Max, Min, and Mean Temperature From 2014 to 2015',
                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
 html.Div(
        'This bubble chart represent the average minimum and maximum temperature each month'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Max and Min Temperature from 2014 to 2015',
                                      xaxis={'title': 'Minimum Temperature'}, yaxis={'title': 'Maximum Temperature'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represent the recorded maximum temperature on a day of a week and month of the year'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Record Max Temperature',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Month of Year'})
              }
              )
])


if __name__ == '__main__':
    app.run_server()
