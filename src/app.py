import pandas as pd
import numpy as np
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Expose the Flask server for Flask commands
server = app.server  

# Data
data = pd.read_csv('../data/raw/pet.csv')

# Layout
app.layout = dbc.Container([
    # Title Row
    dbc.Row(
        dbc.Col(
            html.Div(
                children=[
                    html.H1("Pet Adoption Availability Dashboard", style={'textAlign': 'center', 'marginTop': '20px'}),
                    html.Label('To view pet avaibility by age range, please choose animal hospital, pet type, and adoption status.',
                               style={'textAlign': 'center', 'display': 'block', 'width': '100%', 'margin': '20px', 'fontSize': '18px'})
                ],  
            ), width=12
        ),
        justify="center"
    ),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='hospital-dropdown',
                options=[{'label': h, 'value': h} for h in data['hospital'].unique()],
                value=data['hospital'].unique()[0],
                placeholder='Select Hospital...'
            ),
            width=4
        ),
        dbc.Col(
            dcc.Dropdown(
                id='animal-dropdown',
                options=[{'label': a, 'value': a} for a in data['animal'].unique()],
                value=data['animal'].unique()[0],
                placeholder='Select Pet...'
            ),
            width=4
        ),
        dbc.Col(
            dcc.Dropdown(
                id='status-dropdown',
                options=[{'label': 'All Statuses', 'value': 'All Statuses'},
                         {'label': 'In Adoption Process', 'value': 'In Adoption Process'},
                         {'label': 'Available for Adoption', 'value': 'Available for Adoption'}],
                value=None,
                placeholder='Select Adoption Status...'
            ),
            width=4
        ),
    ], justify="center"),
    html.Div(id='chart-container'),
    html.Div(id='message-container')
])



@app.callback(
    [Output('chart-container', 'children'),
    Output('message-container', 'children')],
    Input('hospital-dropdown', 'value'),
    Input('animal-dropdown', 'value'),
    Input('status-dropdown', 'value'),
)
def update_graph(hospital, animal, status):
    filter_status = True
    if status == 'Available for Adoption':
        filter_status = False
    if status == None or status == 'All Statuses':
        filtered_data = data[(data['hospital'] == hospital) & (data['animal'] == animal)]
    else:
        filtered_data = data[(data['hospital'] == hospital) & (data['animal'] == animal) & (data['in_adoption'] == filter_status)]

    if filtered_data.empty:
        return None, html.Label("No results :/ Please change your selections above.")
    
    filtered_data['has_health_condition'] = filtered_data['has_health_condition'].replace({True: 'Yes', False: 'No'})
  
    age_bins = [0, 1, 4, 7, 10, 14, 18, np.inf]
    age_bin_labels = ['0', '1-3', '4-6', '7-9', '10-13', '14-17', '18+']   
    filtered_data['age_bin'] = pd.cut(filtered_data['age'], bins=age_bins, labels=age_bin_labels, right=False)

    filtered_data['has_health_condition'] = filtered_data['has_health_condition'].astype(str)
    
    age_counts = filtered_data.groupby(['age_bin', 'has_health_condition']).size().reset_index(name='count')
    age_counts = age_counts[age_counts['count'] > 0]
    active_age_bins = age_counts['age_bin'].unique()

    if status == None or status == 'All Statuses':
        status = ''
    if status == 'In Adoption Process':
        status = 'in Adoption Process'
    fig = px.bar(age_counts, x='age_bin', y='count', color='has_health_condition', 
                 labels={'has_health_condition': 'Has Health Condition', 'age_bin': 'Age Range', 'count': 'Number of Pets'}, barmode='stack')

    fig.update_layout(
    title={
        'text': f'{filtered_data.shape[0]} {animal}s in {hospital} {status}',
        'x': 0.5,  
        'xanchor': 'center'  
    },
        xaxis_title="Pet Age",
        yaxis_title="Number of Pets",
        xaxis=dict(
            categoryorder='array',  
            categoryarray=active_age_bins  
        )
    )

    return dcc.Graph(id='chart', figure=fig), None


# Run the app/dashboard
if __name__ == '__main__':
    app.enable_dev_tools(debug=True, dev_tools_hot_reload=True)
    app.run(debug=True, host="127.0.0.1", port=8050, dev_tools_hot_reload=True)