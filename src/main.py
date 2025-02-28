import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import altair as alt
alt.data_transformers.disable_max_rows()
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import plotly.express as px

anime = pd.read_csv("../data/preprocessed_anime.csv")

# { Consts } ---------------------------------------------------------------------------------------------------------------------------- #
root_container_style = {
    'position': 'relative',
    'width': 'calc(100vw - 2rem)', 
    'height': 'calc(100vh - 2rem)',  
    'background-color': '#ECECEC',
    'overflow': 'hidden', 
    'padding': '1rem',
    'box-sizing': 'border-box'
}
filter_container_style = {
    'position': 'relative',
    'width': '100%',
    'maxWidth': '256px',
    'marginBottom': '1rem',
    'height': 'auto',
} 
genre_filter_container_style = {
    'position': 'relative',
    'width': '100%',
    'maxWidth': '256px',
    'marginBottom': '1rem',
    'height': 'auto',
}

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
    date_counts = date_counts.iloc[::30, :]

    # Create the Altair chart
    chart = alt.Chart(date_counts).mark_area().encode(
        color=alt.value('#FFFFFF'),
        x=alt.X('date:T', axis=alt.Axis(grid=False, title=None)),
        y=alt.Y('anime_count:Q', axis=alt.Axis(grid=False, title=None)),
        tooltip=['date:T', 'anime_count:Q']
    ).properties(
        width='container',
        height=100,
        background="#E5E5E5"
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
def generate_radar(df):
    # Explode the Genres column to assign each anime to multiple genres
    df_exploded = df.assign(Genres=df['Genres'].str.split(', ')).explode('Genres')

    # Count the frequency of each genre and select the top 10 most frequent ones
    top_genres = df_exploded['Genres'].value_counts().head(10).index

    # Filter dataset to include only the top 10 genres
    df_exploded = df_exploded[df_exploded['Genres'].isin(top_genres)]

    # Select relevant numerical columns
    columns = ['Score', 'Members', 'Popularity', 'Completed', 'On-Hold', 'Dropped']

    # Aggregate by genre, computing the mean for each variable
    df_genre_avg = df_exploded.groupby('Genres')[columns].mean().reset_index()

    # Normalize values for better visualization (Min-Max Scaling)
    df_genre_avg[columns] = (df_genre_avg[columns] - df_genre_avg[columns].min()) / \
                            (df_genre_avg[columns].max() - df_genre_avg[columns].min())

    # Compute angle for each axis
    num_vars = len(columns)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Close the circle

    # Create the radar chart
    fig = go.Figure()

    # Plot each of the top 10 genres
    for _, row in df_genre_avg.iterrows():
        values = row[columns].values.flatten().tolist()
        values += values[:1]  # Close the circle

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=columns + [columns[0]],
            fill='toself',
            name=row['Genres']
        ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        title="Radar Chart for Top 10 Most Frequent Anime Genres",
        showlegend=True
    )
    
    return fig
def generate_bar(df):
    # Create and process data
    genre_avg_score = df.groupby('Genres')['Score'].mean().reset_index()
    genre_avg_score = genre_avg_score.sort_values(by='Score', ascending=False)
    
    # Take top 5 genres
    top_genres = 10
    bar_height = 30
    chart_height = top_genres * bar_height + 100
    genre_avg_score = genre_avg_score.head(top_genres)
    
    # Create Altair chart
    chart = alt.Chart(genre_avg_score).mark_bar().encode(
        x=alt.X('Score:Q', title='Average Score'),
        y=alt.Y('Genres:N', sort='-x', title='Genre'),
        color=alt.Color('Score:Q', scale=alt.Scale(scheme='blues'), legend=None)
    ).properties(
        title="Average Score by Genre",
        width=600,
        height=chart_height
    )
    
    return chart.to_html()
# { Graph generation functions } ======================================================================================================== #


# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
app = dash.Dash(__name__)
anime_count_by_date = generate_anime_count_by_date(anime)

app.layout = html.Div([
    # Main content container
    html.Div([
        # Top row with radar and bar charts
        html.Div([
            # Left side - Bar chart
            html.Iframe(
                id='bar-chart',
                srcDoc='',
                style={
                    'width': '30%',
                    'height': '400px',
                    'border': 'none',
                    'backgroundColor': '#E5E5E5',
                    'borderRadius': '16px',
                }
            ),
            # heatmap in the middle         
            dcc.Graph(
                id='heatmap-graph',
                style={
                    'width': '30%',
                    'height': '400px',
                }
            ),
            # Right side - Radar chart
            dcc.Graph(
                id='radar-graph',
                style={
                    'width': '30%',
                    'height': '400px',
                    'minWidth': '300px',
                }
            ),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'width': '100%',
            'marginBottom': '0.5rem',
        }),

        # # Center - Heatmap
        # html.Div([
        # ], style={
        #     'display': 'flex',
        #     'justifyContent': 'center',
        #     'width': '100%',
        #     'marginBottom': '2rem',
        # }),

        # Bottom row with filters and time series
        html.Div([
            # Left side - Filters
            html.Div([
                # Type filter
                html.Div([
                    html.Span("Filters", style={'fontSize': '12px', 'fontFamily': 'Arial', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id='type-dropdown',
                        className='dropdown-up',
                        options=[{'label': anime_type, 'value': anime_type} for anime_type in anime['Type'].dropna().unique()],
                        value=anime['Type'].dropna().unique()[0] if not anime['Type'].dropna().empty else None,
                        style={'width': '100%', 'fontSize': '16px', 'fontFamily': 'Arial', 'borderRadius': '8px'},
                        persistence=True,
                        persistence_type='session'
                    )
                ], style=filter_container_style),
                
                # Genre filter
                html.Div([
                    html.Span("Genre Filter", style={'fontSize': '12px', 'fontFamily': 'Arial', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id='genre-dropdown',
                        className='dropdown-up',
                        options=[{'label': 'All', 'value': 'All'}] + [
                            {'label': genre, 'value': genre} 
                            for genre in sorted(set([g.strip() for genres in anime['Genres'].dropna() for g in genres.split(',')]))
                        ],
                        value='All',
                        style={'width': '100%', 'fontSize': '16px', 'fontFamily': 'Arial', 'borderRadius': '8px'},
                        persistence=True,
                        persistence_type='session'
                    )
                ], style=genre_filter_container_style),
            ], style={
                'width': '20%',
                'minWidth': '200px',
                'marginRight': '2rem',
            }),

            # Right side - Time series
            html.Iframe(
                id='area-graph',
                srcDoc=anime_count_by_date,
                style={
                    'width': '75%',
                    'height': '150px',
                    'border': 'none',
                    'backgroundColor': '#E5E5E5',
                    'borderRadius': '16px',
                    'boxShadow': '0 0 16px rgba(0, 0, 0, 0.25)'
                }
            ),
        ], style={
            'display': 'flex',
            'justifyContent': 'flex-start',
            'alignItems': 'center',
            'width': '100%',
            'marginTop': '10rem',
        }),
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100%',
        'padding': '2rem',
    }),
], style=root_container_style)

@app.callback(
    [Output('heatmap-graph', 'figure'),
     Output('radar-graph', 'figure'),
     Output('area-graph', 'srcDoc'),
     Output('bar-chart', 'srcDoc')],
    [Input('type-dropdown', 'value'),
     Input('genre-dropdown', 'value')]
)
def update_graphs(selected_type, selected_genre):
    processed_anime = data_preprocessing(anime, selected_type)
    # genre filter
    if selected_genre:
        # Explode the "Genres" column to separate rows
        processed_anime = processed_anime.assign(Genres=processed_anime['Genres'].str.split(', ')).explode('Genres')
        if selected_genre != 'All':
            processed_anime = processed_anime[processed_anime['Genres'] == selected_genre]
    heatmap_graph = generate_heatmap(processed_anime)
    radar_graph = generate_radar(processed_anime)
    area_graph = generate_anime_count_by_date(processed_anime)
    bar_chart = generate_bar(processed_anime)
    return heatmap_graph, radar_graph, area_graph, bar_chart

if __name__ == '__main__':
    app.run_server(debug=False)
# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
