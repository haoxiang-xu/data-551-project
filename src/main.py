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
from sklearn.preprocessing import LabelEncoder
from plotly.subplots import make_subplots
from pycountry_convert import country_name_to_country_alpha2, country_alpha2_to_continent_code

# { npm components } -------------------------------------------------------------------------------------------------------------------- #
import dtl
import selector
import bar_plt
import widgets
import radar
import heatmap
# { npm components } -------------------------------------------------------------------------------------------------------------------- #

anime = pd.read_csv("../data/preprocessed_anime.csv")
# sampling
anime = anime.sample(n=3000, random_state=42)

# Load data for map component.
df_viewers = pd.read_csv("../data/anime_viewers_cleaned.csv")
df_viewers = df_viewers[df_viewers["viewers"] >= 100]

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
# anime['start_date'] = pd.to_datetime(anime['start_date'])
# anime['end_date'] = pd.to_datetime(anime['end_date'])
def data_preprocessing(df, selected_filters=None):
    df = df.copy()
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    if selected_filters[0] and selected_filters[0] != 'All':
        df = df[df['Type'] == selected_filters[0]]
            
    if selected_filters[2]:
        if selected_filters[2] != 'All':
            df = df[df['Studios'] == selected_filters[2]]
    
    # make sure the explode is done after type and studio filter
    df = df.assign(Genres=df['Genres'].str.split(', ')).explode('Genres')

    # make sure the genre filter happen after the explode
    if selected_filters[1]:
        if selected_filters[1] != 'All':
            df = df[df['Genres'] == selected_filters[1]]    

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
    # copy the dataframe
    df = df.copy().fillna(0)
    
    # Explode Genres with comma (assuming multi-genre entries)
    df = df.assign(Genres=df['Genres'].str.split(', ')).explode('Genres')
    
    # Convert Aired to datetime and extract year
    df['Aired'] = pd.to_datetime(df['Aired'], errors='coerce')
    df['Aired'] = df['Aired'].dt.year
    
    # Define important columns
    important_columns = ['Genres', 'Type', 'Episodes', 'Aired', 'Studios', 'Members', 'Score', 'Popularity']
    df_subset = df[important_columns].dropna()
    
    # Convert categorical columns to integers using LabelEncoder
    le = LabelEncoder()
    df_subset['Genres'] = le.fit_transform(df_subset['Genres'])
    df_subset['Type'] = le.fit_transform(df_subset['Type'])
    df_subset['Studios'] = le.fit_transform(df_subset['Studios'])

    # negate the popularity for making it more intuitive for ranking
    df_subset['Popularity'] = -df_subset['Popularity']
    
    # Define target variables
    target_vars = ['Score', 'Popularity']
    
    # Get all columns for correlation
    all_columns = df_subset.columns
    
    # Calculate correlation matrix
    correlation_matrix = df_subset[all_columns].corr()
    correlation_matrix = correlation_matrix.fillna(0)
    
    # Filter out the row with column and column with target variables   
    corr_with_targets = correlation_matrix.loc[all_columns, target_vars]
    
    # Convert to JSON-like dictionary
    correlation_json = corr_with_targets.copy().round(2).to_dict()
    
    return heatmap.Heatmap(
        id='dash-heatmap',
        data=correlation_json,
    )
def generate_radar(df):
    df_exploded = df.assign(Genres=df['Genres'].str.split(', ')).explode('Genres')

    # Count the frequency of each genre and select the top 10 most frequent ones
    top_genres = df_exploded['Genres'].value_counts().head(10).index

    # Filter dataset to include only the top 10 genres
    df_exploded = df_exploded[df_exploded['Genres'].isin(top_genres)]

    # Select relevant numerical columns
    columns = ['Score', 'Members', 'Popularity', 'Completed', 'On-Hold', 'Dropped']

    # Aggregate by genre, computing the mean for each variable
    df_genre_avg_original = df_exploded.groupby('Genres')[columns].mean().reset_index()

    # Store the original mean data before normalization
    df_genre_avg = df_genre_avg_original.copy()

    # Normalize values for better visualization (Min-Max Scaling)
    df_genre_avg[columns] = (df_genre_avg[columns] - df_genre_avg[columns].min()) / \
                            (df_genre_avg[columns].max() - df_genre_avg[columns].min())

    json_data = [
        {
            "genre": row["Genres"],
            "Score": round(row["Score"], 3),
            "Members": round(row["Members"], 3),
            "Popularity": round(row["Popularity"], 3),
            "Completed": round(row["Completed"], 3),
            "OnHold": round(row["On-Hold"], 3),
            "Dropped": round(row["Dropped"], 3),
        }
        for _, row in df_genre_avg.iterrows()
    ]

    return radar.Radar(
        id='dash-radar-chart',
        data=json_data,
    )
def generate_bar(df):
    # Create and process data
    genre_avg_score = df.groupby('Genres')['Score'].mean().round(2).reset_index()
    # sort by score descending
    genre_avg_score = genre_avg_score.sort_values(by='Score', ascending=False)
    
    # Take top 10 genres (keeping it consistent with your original)
    top_genres = 10
    bar_height = 30
    genre_avg_score = genre_avg_score.head(top_genres)
    
    res = [{'genre': row['Genres'], 'score': row['Score']} for index, row in genre_avg_score.iterrows()]
    
    return bar_plt.BarPlt(
        id='dash-bar-chart',
        data=res,
    )
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


        return x[::3], y[::3]
    def generate_average_score_by_date(df):
        df = df.iloc[::60, :].copy()
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
    
    if count_x[0] < score_x[0]:
        score_x.insert(0, count_x[0])
        score_y.insert(0, 0)
    elif count_x[0] > score_x[0]:
        count_x.insert(0, score_x[0])
        count_y.insert(0, 0)

    # Ensure the end range matches
    if count_x[-1] > score_x[-1]:
        score_x.append(count_x[-1])
        score_y.append(0)
    elif count_x[-1] < score_x[-1]:
        count_x.append(score_x[-1])
        count_y.append(0)
    
    return dtl.Dtl(
        id='dash-timeline',
        countX=count_x,
        countY=count_y,
        scoreX=score_x,
        scoreY=score_y
    )
def generate_widgets(df):
    def get_top_3_animes(df):
        top_scores = (
            df.dropna(subset=['Name', 'Score'])
            .sort_values(by='Score', ascending=False)
            .drop_duplicates(subset='Name')
            .head(3)[['Name', 'Score']])
    
        return [{"title": row["Name"], "score": f"{row['Score']:.2f}"} for _, row in top_scores.iterrows()]

    def get_average_score(df):
        return round(df["Score"].mean(), 2)
    
    top_3_animes = get_top_3_animes(df)
    average_score = get_average_score(df)
    
    return widgets.Widgets(
        id='dash-widgets',
        top_3=top_3_animes,
        average_score=average_score
    )

# { Map component } ------------------------------------------------------------------------------------------------------------------------ #
# def get_continent(country):
    """
    Get the continent of a country.
    """
    try:
        country_code = country_name_to_country_alpha2(country)
        continent_code = country_alpha2_to_continent_code(country_code)
        continent_map = {
            "NA": "North America",
            "SA": "South America",
            "EU": "Europe",
            "AF": "Africa",
            "AS": "Asia",
            "OC": "Oceania",
        }
        return continent_map.get(continent_code, "Other")
    except:
        return "Unknown"

# Apply function to get continent
# df_viewers["continent"] = df_viewers["country"].apply(get_continent)
# df_viewers = df_viewers[df_viewers["continent"] != "Unknown"]

# # Get top countries per continent
# top_countries = df_viewers.loc[df_viewers.groupby("continent")["viewers"].idxmax()]

# # Define continent zoom settings
# continent_scopes = {
#     "North America": "north america",
#     "South America": "south america",
#     "Europe": "europe",
#     "Asia": "asia",
#     "Africa": "africa"
# }

# # Define positions in subplots
# continent_positions = {
#     "North America": (1, 1),
#     "South America": (1, 2),
#     "Europe": (2, 1),
#     "Asia": (2, 2),
#     "Africa": (3, 1),
#     "Oceania": (3, 2),
# }

def generate_global_viewers_map():
    """
    Generate a map of the global anime viewers with full width and height.
    """
    fig = go.Figure(
        data=go.Choropleth(
            locations=df_viewers["country"],
            locationmode="country names",
            z=df_viewers["viewers"],
            colorscale="YlOrRd",
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title="Viewers",
        )
    )
 
    fig.update_layout(
        autosize=False,  # Enables automatic resizing
        width=None,  
        height=None,  
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type="natural earth"
        ),
        title_font_size=18
    )
 
    return fig
# { Graph generation functions } ======================================================================================================== #

# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
# initialize dash app
app = dash.Dash(__name__)

app.layout = html.Div([
html.Div([
    dcc.Graph(
        id='global-viewers-map',
        style={
            'position': 'absolute',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'margin': '0',
            'padding': '0'
        }
    )
], style={
    'position': 'absolute',
    'top': '216px',
    'left': '18px',
    'width': 'calc(66% - 36px)',
    'bottom': '186px',
    'overflow': 'hidden',
    'background-color': 'white',
    'border-radius': '4px',
    'box-shadow': '0 0 10px rgba(0, 0, 0, 0.1)',
    'margin': '0',
    'padding': '0'
}),
    html.Div(id='dash-radar-chart-container'),
    html.Div(id='dash-timeline-container'),
    html.Div(id='dash-bar-chart-container'),
    html.Div(id='dash-widgets-container'),
    html.Div(id='dash-heatmap-container'),
    selector.Selector(
        id='selector',
        values=['All', 'All', 'All'],
        typeOptions=type_options,
        genreOptions=genre_options,
        studioOptions=studio_options    
    ),
], style=root_container_style)

@app.callback(
    [Output('dash-heatmap-container', 'children'),
     Output('dash-radar-chart-container', 'children'),
     Output('dash-bar-chart-container', 'children'),
     Output('dash-timeline-container', 'children'),
     Output('dash-widgets-container', 'children'),
     Output('global-viewers-map', 'figure')],
    [Input('selector', 'values')]
)
def update_graphs(selected_filters):
    processed_anime = data_preprocessing(anime, selected_filters)
    heatmap_graph = generate_heatmap(processed_anime)
    radar_graph = generate_radar(processed_anime)
    bar_chart = generate_bar(processed_anime)
    time_line_graph = generate_timeline_component(processed_anime)
    widgets = generate_widgets(processed_anime)
    global_viewers_map = generate_global_viewers_map()
    return heatmap_graph, radar_graph, bar_chart, time_line_graph, widgets, global_viewers_map

if __name__ == '__main__':
    app.run_server(debug=False)
# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
