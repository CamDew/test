# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 10:23:12 2024

@author: camde
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
from sklearn.linear_model import LinearRegression
from random import gauss
import math
import requests
import datetime
import random
from dash import  Input, Output, callback

# Define your API endpoint
api_uri = 'https://tzui4wlphi.execute-api.us-east-1.amazonaws.com/prod/courses/'

# Fetch data from the API
response = requests.get(api_uri)

# Check if the request was successful
if response.status_code == 200:
    courses_data = response.json()
    print("Data fetched successfully!")
else:
    print(f"Failed to fetch data: {response.status_code}")
    courses_data = []

# Normalize the data to extract reviews for each course
courses = []
for course in courses_data:
    for review in course.get('reviews', []):
        courses.append({
            'Course ID': course['courseId'],
            'Course Name': course['title'],
            'Rating': review['overall'],
            'Course Difficulty': review['difficulty'],
            'Course Usefulness': review['usefulness'],
            'Major': review['major'],
            'Is Anonymous': review['anonymous'],
            'Additional Comments': review['additionalComments'],
            'Tips': review['tips'],
            'Professor': review['professor'],
            'Date': review['createdAt']  # Assuming there's a createdAt field for the date
        })

# Create a DataFrame from the extracted data
df1 = pd.DataFrame(courses)
df1['Course ID'] = df1['Course ID'].str.upper()
df1['Course Name'] = df1['Course Name'].str.upper()
df1['Major'] = df1['Major'].str.upper()
df1['Professor'] = df1['Professor'].str.upper()

pio.templates.default = "plotly_white"

fig1 = px.pie(df1, names='Major', opacity=0.65,title="Breakdown of Majors")
fig2 = px.scatter(df1,x='Rating', y = 'Course Difficulty', opacity=0.65, title = "Overall Rating vs Difficulty", 
                  hover_data=['Course Difficulty','Course Usefulness','Major'],trendline = 'ols', marginal_x= 'box',marginal_y= 'box')
fig3 = px.histogram(df1,x='Rating', facet_row = 'Is Anonymous',title = "Overall Rating Distribution by Anonymity Status",color = 'Is Anonymous')
fig4 = px.scatter_3d(df1,x='Rating', y = 'Course Difficulty', z = 'Course Usefulness' ,title = 'Difficulty vs Usefulness vs Rating',color = 'Is Anonymous')
fig5 = px.scatter_matrix(df1, dimensions=["Course Difficulty", "Rating", "Course Usefulness"], color = 'Is Anonymous', title = 'Relationships Between Review Metrics')
app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

plot_bgcolor=colors['background']
app.layout = html.Div(children=[
        html.Div(
            children=[
                html.H1(
                    children="Analysis of Course Reviews",style={'textAlign': 'left'}, className="header-title" 
                ), #Header title
                html.H3(
                    children="A Look at Data from Course Review Posts",
                    className="header-description", style={'textAlign': 'left'},
                ),
            ],
            className="header",style={},
        ), #Description below the header
        html.Div(
            children=[
                    html.Div([
                     dcc.Dropdown(options=[{'label': 'Select All', 'value': 'all'}] + [{'label': i, 'value': i} for i in df1['Course Name'].unique()],
                                  value=['all'],multi = True,id='dropdown'),
                     html.Div(id='output-container')]),
                html.Div(
                children = dcc.Graph(
                    id = 'g5',
                    figure = fig5,
                  #  config={"displayModeBar": False},
                ),
                style={'width': '100%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'g1',
                    figure = fig1,
                  #  config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'g2',
                    figure = fig2,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'g3',
                    figure = fig3,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'g4',
                    figure = fig4,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                
            ],

        className = 'double-graph',
        )
]
) 
@callback(
    Output('g1', 'figure'),
    Output('g2', 'figure'),
    Output('g3', 'figure'),
    Output('g4', 'figure'),
    Output('g5', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(selected_course):
    if selected_course == 'all':
    #    selected_course = df1['Course Name'].unique()
    #dff = df1[df1['Course Name'].isin(selected_course)]
        dff = df1
    else:
        dff = df1[df1['Course Name'].isin(selected_course)]
        #dff = df1[df1['Course Name'] == selected_course]
    fig1 = px.pie(dff, names='Major', opacity=0.65,title="Breakdown of Majors")
    fig2 = px.scatter(dff,x='Rating', y = 'Course Difficulty', opacity=0.65, title = "Overall Rating vs Difficulty", 
                  hover_data=['Course Difficulty','Course Usefulness','Major'],trendline = 'ols', marginal_x= 'box',marginal_y= 'box')
    fig3 = px.histogram(dff,x='Rating', facet_row = 'Is Anonymous',title = "Overall Rating Distribution by Anonymity Status",color = 'Is Anonymous')
    fig4 = px.scatter_3d(dff,x='Rating', y = 'Course Difficulty', z = 'Course Usefulness' ,title = 'Difficulty vs Usefulness vs Rating',color = 'Is Anonymous')
    fig5 = px.scatter_matrix(dff, dimensions=["Course Difficulty", "Rating", "Course Usefulness"], color = 'Is Anonymous', title = 'Relationships Between Review Metrics')
    fig1.update_layout(transition_duration=500)
    fig2.update_layout(transition_duration=500)
    fig3.update_layout(transition_duration=500)
    fig4.update_layout(transition_duration=500)
    fig5.update_layout(transition_duration=500)
    return fig1, fig2, fig3, fig4, fig5
#if not using virtual environment
#dashboard is hosted at http://127.0.0.1:8050/
if __name__ == '__main__':
     app.run_server()
                
