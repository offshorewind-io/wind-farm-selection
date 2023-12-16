import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

def clean_coord(value):
    if isinstance(value, str):
        value = value.replace("°", "").replace("'", "").replace('"', "")
    try:
        return float(value)
    except ValueError:
        return None

# Read the data
file_path = 'Wind farm overview.xlsx' 
df = pd.read_excel(file_path)

# Clean data
df['latitude'] = df['latitude'].apply(clean_coord)
df['longitude'] = df['longitude'].apply(clean_coord)
df.dropna(subset=['latitude', 'longitude'], inplace=True)

data_columns = ['country', 
                'turbine_model',
                'turbine_capacity_MW',
                'windfarm_capacity_MW',
                'number_turbines',
                'full_commissioning_year',
                'foundation_type',
                'distance_from_shore',
                ]

fig_map = px.scatter_geo(df, lat='latitude', lon='longitude', projection="natural earth", hover_name='name', hover_data=data_columns)
fig_histogram = px.histogram(df, x='country')
df_table = df[['name'] + data_columns]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    html.H1("Card deck wind farm selection"),
    dcc.Graph(figure=fig_map),
    dbc.Select(data_columns, "country", id="shorthand-select", style={'width': 700}),
    dcc.Graph(figure=fig_histogram, id="fig-histogram"),
    dash_table.DataTable(df_table.to_dict('records'))
],
style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
    }
)

@app.callback([Output('fig-histogram', 'figure')], [Input('shorthand-select', 'value')])
def update_histogram(column):
    fig_histogram = px.histogram(df, x=column)
    return (fig_histogram,)


if __name__ == '__main__':
    app.run_server(debug=True)  
