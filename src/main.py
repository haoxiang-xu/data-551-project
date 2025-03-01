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
import dtl
import selector

anime = pd.read_csv("../data/preprocessed_anime.csv")

# { Consts } ---------------------------------------------------------------------------------------------------------------------------- #
root_container_style = {
    'position': 'absolute',
    'top': '0',
    'left': '0',
    'right': '0',
    'bottom': '0',
    'background-color': '#ECECEC',
    'overflow': 'hidden',
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

# list of string
type_options = ['All'] + [anime_type for anime_type in anime['Type'].dropna().unique()]
genre_options = ['All'] + sorted(set([g.strip() for genres in anime['Genres'].dropna() for g in genres.split(',')]))
studio_options = ['All'] + sorted(set([s.strip() for studios in anime['Studios'].dropna() for s in studios.split(',')]))
# { Consts } ---------------------------------------------------------------------------------------------------------------------------- #

# { Data preprocessing } ---------------------------------------------------------------------------------------------------------------- # 
anime['start_date'] = pd.to_datetime(anime['start_date'])
anime['end_date'] = pd.to_datetime(anime['end_date'])
def data_preprocessing(df, selected_filters=None):
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    if selected_filters[0] and selected_filters[0] != 'All':
        df = df[df['Type'] == selected_filters[0]]
        
    if selected_filters[1]:
        df = df.assign(Genres=df['Genres'].str.split(', ')).explode('Genres')
        if selected_filters[1] != 'All':
            df = df[df['Genres'] == selected_filters[1]]
            
    if selected_filters[2]:
        df = df.assign(Studios=df['Studios'].str.split(', ')).explode('Studios')
        if selected_filters[2] != 'All':
            df = df[df['Studios'] == selected_filters[2]]

    return df
# { Data preprocessing } ---------------------------------------------------------------------------------------------------------------- # 

# { Graph generation functions } ======================================================================================================== #
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
def generate_timeline_component(df):
    def generate_anime_count_by_date(df):
        all_dates = []
        
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
        df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
        
        df = df.dropna(subset=['start_date', 'end_date'])
        
        for _, row in df.iterrows():
            date_range = pd.date_range(row['start_date'], row['end_date'], freq='D')
            all_dates.extend(date_range)
            
        date_counts = pd.DataFrame(all_dates, columns=['date'])
        date_counts = date_counts.groupby('date').size().reset_index(name='anime_count')
        date_counts = date_counts.iloc[::30, :]

        date_counts = date_counts.to_numpy()
        date_counts = np.array(date_counts)
        date_counts = date_counts.tolist()
        
        x = []
        y = []

        for i in date_counts:
            x.append(str(i[0])[:10])
            y.append(i[1])


        return x[::7], y[::7]
    def generate_average_score_by_date(df):
        df = df.iloc[::60, :]
        df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
        
        all_dates_scores = []
        for _, row in df.iterrows():
            date_range = pd.date_range(row['start_date'], row['end_date'], freq='D')
            all_dates_scores.extend([(date, row['Score']) for date in date_range])

        # Convert to DataFrame and calculate average score per date
        date_scores_df = pd.DataFrame(all_dates_scores, columns=['date', 'score'])
        average_scores = date_scores_df.groupby('date').agg(
            avg_score=('score', 'mean'),
            anime_count=('score', 'count')
        ).reset_index()

        average_scores
        #break into x and y x is date y is avg_score both are arrays
        # convert date to string only date part
        x = average_scores['date'].tolist()
        x = [str(i).split
            (' ')[0] for i in x]
        y = average_scores['avg_score'].tolist()
        
        return x[::7], y[::7]
    
    count_x, count_y = generate_anime_count_by_date(df)
    score_x, score_y = generate_average_score_by_date(df)
    
    return dtl.Dtl(
        id='dash-timeline',
        countX=count_x,
        countY=count_y,
        scoreX=score_x,
        scoreY=score_y
    )
# { Graph generation functions } ======================================================================================================== #


# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
app = dash.Dash(__name__)

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
    ], style={
        'position': 'absolute',
        'top': '0',
        'left': '0',
        'right': '0',
        'bottom': '0',
    }),
    html.Div(id='dash-timeline-container'),
    selector.Selector(
        id='selector',
        values=['All', 'All', 'All'],
        typeOptions=type_options,
        genreOptions=genre_options,
        studioOptions=studio_options    
    ),
], style=root_container_style)

@app.callback(
    [Output('heatmap-graph', 'figure'),
     Output('radar-graph', 'figure'),
     Output('bar-chart', 'srcDoc'),
    Output('dash-timeline-container', 'children')],
    [Input('selector', 'values')]
)
def update_graphs(selected_filters):
    processed_anime = data_preprocessing(anime, selected_filters)
    heatmap_graph = generate_heatmap(processed_anime)
    radar_graph = generate_radar(processed_anime)
    bar_chart = generate_bar(processed_anime)
    time_line_graph = generate_timeline_component(processed_anime)
    return heatmap_graph, radar_graph, bar_chart, time_line_graph

if __name__ == '__main__':
    app.run_server(debug=False)
# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
