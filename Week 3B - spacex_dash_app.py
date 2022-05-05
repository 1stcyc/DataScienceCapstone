# import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# read the spacex data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# get the list of sites
sites = spacex_df['Launch Site'].unique().tolist()

# create a dash application
app = dash.Dash(__name__)

# create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
### Task 1 Code ###
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': sites[0],    'value': sites[0]},
                                                 {'label': sites[1],    'value': sites[1]},
                                                 {'label': sites[2],    'value': sites[2]},
                                                 {'label': sites[3],    'value': sites[3]},
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                            ),
### Task 1 Code ###
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range

### Task 3 Code ###
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 100: '100'},
                                                value=[min_payload, max_payload]
                                               ),
### Task 3 Code ###
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

### Task 2 Code ###

# add callback decorator to specify function input and output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input( component_id='site-dropdown',     component_property='value'))
# add codes to callback function and return the pie chart
def get_pie_chart(entered_site):
    df = spacex_df
    if entered_site == 'ALL':
        # return the success outcomes piechart for all sites
        fig = px.pie(df, values='class',  
        names = 'Launch Site', 
        title = 'Total Success Launches by Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        dfx = df[df['Launch Site'] == entered_site]
        dfg = dfx['class'].value_counts().rename_axis('class').reset_index(name='counts')
        fig = px.pie(dfg, values='counts',  
        names = 'class', 
        title = 'Total Success Launches for Site ' + entered_site)
        return fig

### Task 2 Code ###

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

### Task 4 Code ###

@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               Input( component_id='site-dropdown',                 component_property='value'),
               Input( component_id='payload-slider',                component_property='value'))
def get_scatter_chart(entered_site, payload_minmax):
    df = spacex_df
    if entered_site == 'ALL':
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        dfx = df[(df['Launch Site']==entered_site) & 
                 (df['Payload Mass (kg)']>=payload_minmax[0]) & 
                 (df['Payload Mass (kg)']<=payload_minmax[1])]
        fig = px.scatter(dfx, x='Payload Mass (kg)', y='class', color='Booster Version',
                         title='Correlation between Payload and Success for site ' + entered_site)
        return fig

### Task 4 Code ###

# run the app
if __name__ == '__main__':
    app.run_server()
