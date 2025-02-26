import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import altair as alt
alt.data_transformers.disable_max_rows()
import pandas as pd
import numpy as np
import plotly.graph_objects as go

anime = pd.read_csv("../data/preprocessed_anime.csv")

# { Consts } ---------------------------------------------------------------------------------------------------------------------------- #
root_container_style = {
    'position': 'absolute',
    'top': '0',
    'left': '0',
    'width': '100%',
    'height': '100%',
    'background-color': '#ECECEC',
    'overflow': 'hidden',
}
filter_container_style = {
    'position': 'absolute',
    'bottom': '96px',
    'left': '18px',
    'width': '256px',
    'height': '128px',
} 
# { Consts } ---------------------------------------------------------------------------------------------------------------------------- #

# { Data preprocessing } ---------------------------------------------------------------------------------------------------------------- # 
anime['start_date'] = pd.to_datetime(anime['start_date'])
anime['end_date'] = pd.to_datetime(anime['end_date'])
def data_preprocessing(df, selected_type=None):
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    if selected_type and selected_type != 'All':
        df = df[df['Type'] == selected_type]

    return df
# { Data preprocessing } ---------------------------------------------------------------------------------------------------------------- # 

# { Graph generation functions } ======================================================================================================== #
def generate_anime_count_by_date(df):
    all_dates = []
    
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
    
    df = df.dropna(subset=['start_date', 'end_date'])
    
    for _, row in df.iterrows():
        date_range = pd.date_range(row['start_date'], row['end_date'], freq='D')
        all_dates.extend(date_range)

    # Convert to DataFrame and count occurrences
    date_counts = pd.DataFrame(all_dates, columns=['date'])
    date_counts = date_counts.groupby('date').size().reset_index(name='anime_count')

    # Create the Altair chart
    chart = alt.Chart(date_counts).mark_area().encode(
        x=alt.X('date:T', axis=alt.Axis(grid=False, title=None)),
        y=alt.Y('anime_count:Q', axis=alt.Axis(grid=False, title=None)),
        tooltip=['date:T', 'anime_count:Q']
    ).properties(
        width='container',
        height=100
    ).configure_view(
        strokeWidth=0,
        fill="#00000000"
    ).configure_axis(
        grid=False  # Removes all grid lines
    )
    
    chart.configure_view(strokeWidth=0)
    return chart.to_html()
def generate_heatmap(df):
    """
    Create a correlation heatmap based on filtered data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The anime dataset
    selected_type : str, optional
        The type of anime to filter by (e.g., 'TV', 'Movie', etc.)
    """
    # Define numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns

    # Calculate correlation matrix
    correlation_matrix = df[numeric_columns].corr()
    
    # Heatmap creation
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=numeric_columns,
        y=numeric_columns,
        hoverongaps=False,
        zmin=-1, zmax=1,
        colorscale=[
            [0, "rgb(240, 240, 255)"],  # Light Blue
            [0.5, "rgb(180, 180, 250)"],  # Medium Blue
            [1, "rgb(120, 120, 200)"]  # Darker Blue
        ],
        text=np.round(correlation_matrix, 2),
        texttemplate='%{text}',
        textfont={"size": 12},
        showscale=False,  # Hide the color scale for a clean look
    ))

    # Layout adjustments to match the uploaded style
    fig.update_layout(
        xaxis_title="Metrics",
        yaxis_title="Metrics",
        height=500,  # Reduce height to be more square-like
        width=500,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False  # Hide axis labels
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False  # Hide axis labels
        ),
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
    )

    return fig
# { Graph generation functions } ======================================================================================================== #


# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
app = dash.Dash(__name__)
anime_count_by_date = generate_anime_count_by_date(anime)

app.layout = html.Div([
    html.Div([
        html.Span("Filters", style={'position': 'absolute', 'top': '0', 'left': '0', 'font-size': '24px', 'font-family': 'Arial'}),
        dcc.Dropdown(
            id='type-dropdown',
            className='dropdown-up',  # Link to the CSS class
            options=[{'label': anime_type, 'value': anime_type} for anime_type in anime['Type'].dropna().unique()],
            value=anime['Type'].dropna().unique()[0] if not anime['Type'].dropna().empty else None,
            style={'position': 'absolute', 'top': '16px', 'left': '0', 'width': '100%', 'font-size': '16px', 'font-family': 'Arial', 'border-radius': '8px'},
            persistence=True,  # Keeps the selected value persistent across callbacks
            persistence_type='session'
        )
    ], style=filter_container_style),
    dcc.Graph(id='heatmap-graph', style={'position': 'absolute', 'top': '50%', 'left': '50%', 'width': '500px', 'height': '500px', 'transform': 'translate(-50%, -50%)'}),
    html.Iframe(id='area-graph', srcDoc=anime_count_by_date, style={'position': 'absolute', 'bottom': '0', 'left': '274px', 'width': 'calc(100% - 300px)' , 'height': '150px', 'border': 'none'})
], style=root_container_style)

@app.callback(
    [Output('heatmap-graph', 'figure'),
     Output('area-graph', 'srcDoc')],
    [Input('type-dropdown', 'value')]
)
def update_graphs(selected_type):
    
    processed_anime = data_preprocessing(anime, selected_type)
    heatmap_graph = generate_heatmap(processed_anime)
    area_graph = generate_anime_count_by_date(processed_anime)
    return heatmap_graph, area_graph

if __name__ == '__main__':
    app.run_server(debug=False)
# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
