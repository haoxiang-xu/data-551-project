import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample Data
df = px.data.iris()  # Built-in dataset

# Create Dash App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Interactive Plot Example"),
    dcc.Dropdown(
        id='species-dropdown',
        options=[{'label': species, 'value': species} for species in df['species'].unique()],
        value=df['species'].unique()[0]
    ),
    dcc.Graph(id='scatter-plot')  # Plot
])

# Callback for updating plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('species-dropdown', 'value')
)
def update_plot(selected_species):
    filtered_df = df[df['species'] == selected_species]
    fig = px.scatter(filtered_df, x="sepal_width", y="sepal_length", title=f"{selected_species} Sepal Dimensions")
    return fig

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)