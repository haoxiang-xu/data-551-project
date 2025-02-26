import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
from vega_datasets import data

# Sample Data
df = data.iris()

# Create Dash App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Interactive Altair Plot Example"),
    dcc.Dropdown(
        id='species-dropdown',
        options=[{'label': species, 'value': species} for species in df['species'].unique()],
        value=df['species'].unique()[0]
    ),
    html.Iframe(id='scatter-plot', style={'width': '100%', 'height': '500px', 'border': 'none'})
])

# Callback for updating plot
@app.callback(
    Output('scatter-plot', 'srcDoc'),
    Input('species-dropdown', 'value')
)
def update_plot(selected_species):
    filtered_df = df[df['species'] == selected_species]
    chart = alt.Chart(filtered_df).mark_circle().encode(
        x='sepalWidth',
        y='sepalLength',
        tooltip=['sepalWidth', 'sepalLength']
    ).properties(title=f"{selected_species} Sepal Dimensions").interactive()
    return chart.to_html()

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)

