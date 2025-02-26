import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import altair as alt
alt.data_transformers.disable_max_rows()
import pandas as pd

anime = pd.read_csv("../data/preprocessed_anime.csv")

# { Consts } ---------------------------------------------------------------------------------------------------------------------------- #
root_container_style = {
    'position': 'absolute',
    'top': '0',
    'left': '0',
    'width': '100%',
    'height': '100%',
    'background-color': '#ECECEC',
}
filter_container_style = {
    'position': 'absolute',
    'bottom': '18px',
    'left': '18px',
    'width': '256px',
    'height': '256px',
    'background-color': '#FFFFFF',
} 
# { Consts } ---------------------------------------------------------------------------------------------------------------------------- #

# { Data preprocessing } ---------------------------------------------------------------------------------------------------------------- # 
anime['start_date'] = pd.to_datetime(anime['start_date'])
anime['end_date'] = pd.to_datetime(anime['end_date'])
# { Data preprocessing } ---------------------------------------------------------------------------------------------------------------- # 

# { Graph generation functions } ======================================================================================================== #
def generate_anime_count_by_date(anime):
    all_dates = []
    
    anime['start_date'] = pd.to_datetime(anime['start_date'], errors='coerce')
    anime['end_date'] = pd.to_datetime(anime['end_date'], errors='coerce')
    
    anime = anime.dropna(subset=['start_date', 'end_date'])
    
    for _, row in anime.iterrows():
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
def generate_heatmap(df, selected_type=None):
    """
    Create a correlation heatmap based on filtered data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The anime dataset
    selected_type : str, optional
        The type of anime to filter by (e.g., 'TV', 'Movie', etc.)
    """
    # Filter data if type is selected
    if selected_type and selected_type != 'All':
        df = df[df['Type'] == selected_type]
    
    # Calculate correlation matrix
    correlation_matrix = df[numeric_columns].corr()
    
    # heatmap creation
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=numeric_columns,
        y=numeric_columns,
        hoverongaps=False,
        # define the max and min for the correlation value
        zmin=-1,
        zmax=1,
        colorscale='RdBu',
        text=np.round(correlation_matrix, 2),
        # correlation value here
        texttemplate='%{text}',
        textfont={"size": 12},
        showscale=True
    ))
    
    # heatmap layout
    fig.update_layout(
        title=f'Anime Correlation Heatmap {f"- {selected_type}" if selected_type else ""}',
        xaxis_title="Metrics",
        yaxis_title="Metrics",
        height=800,
        width=900
    )
    
    return fig
# { Graph generation functions } ======================================================================================================== #


# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
app = dash.Dash(__name__)
anime_count_by_date = generate_anime_count_by_date(anime)

app.layout = html.Div([
    html.Div([
        html.Span("Filters", style={'position': 'absolute', 'top': '0', 'left': '0', 'font-size': '24px'}),
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': anime_type, 'value': anime_type} for anime_type in anime['Type'].dropna().unique()],
            value=anime['Type'].dropna().unique()[0] if not anime['Type'].dropna().empty else None,
            style={'position': 'absolute', 'top': '32px', 'left': '0', 'width': '100%'}
        ),
    ], style=filter_container_style),
], style=root_container_style)

@app.callback(
    Output('scatter-plot', 'srcDoc'),
    Input('interval-component', 'n_intervals')  # ✅ Trigger updates every 10 seconds
)
def update_plot(selected_species):
    return generate_anime_count_by_date(anime)

if __name__ == '__main__':
    app.run_server(debug=False)
# { Dash App } -------------------------------------------------------------------------------------------------------------------------- #
