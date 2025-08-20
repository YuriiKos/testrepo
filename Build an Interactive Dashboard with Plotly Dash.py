# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
#Task 1 - done
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',  
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),
    html.Br(),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        value='ALL',
        placeholder="Select site",
        searchable=True
    ),
    html.Br(),
    dcc.Graph(id='success-pie-chart'),
       dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        },
        value=[0, 10000]  # Example start values
    ),
    dcc.Graph(id='success-payload-scatter-chart')
])
# Task 2 Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # If 'ALL' is selected, show overall success vs. failure counts
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='class',  # Show total successful vs failed launches
            title='Total Success vs Failure Launches (All Sites)',
        )
        return fig
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',  # Show success vs failure for this site
            title=f'Success vs Failure Launches for site {entered_site}',
        )
        return fig
        
# Task 3: Add a RangeSlider for payload mass selection
dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    marks={
        0: '0',
        2500: '2500',
        5000: '5000',
        7500: '7500',
        10000: '10000'
    },
    value=[0,10000]  # Replace min_value and max_value with your desired initial range
)

# Task 4 
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_chart(selected_site, selected_payload_range):
    low, high = selected_payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites'
        )
    else:
        df_site = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            df_site,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {selected_site}'
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()

