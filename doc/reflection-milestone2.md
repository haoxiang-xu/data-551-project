# Reflection for Milestone 2

For Milestone 2, we’ve developed a working prototype of our "Anime Popularity & Ratings Dashboard" using Kaggle data. This tool assists anime companies, studios, and investors in identifying factors driving anime success—such as genre, studio, and release timing—to improve profitability.

## Implemented Features
The dashboard currently includes:
- A **heat map** showing correlations between predictors and outcomes (popularity, ratings). It’s the core visualization, highlighting key influences in different categories predictors(e.g., genre, type, studio).
- A **bar chart** displaying average ratings by genre, offering clear insights into genre performance.
- A **time-series plot** with a slider filter, allowing users to explore trends over time and identify optimal release windows.
- A **radar chart** comparing multiple metrics (e.g., number of completed, dropped, score) across genres or studios or anime types.
- **Filters** for genres, types, and studios, linked to the bar chart, time-series plot, heat map, and radar chart for basic interactivity.

These elements align with the layout sketched in our README, with the heat map as the centerpiece surrounded by supporting charts.

## Not Yet Implemented
Some planned features remain in progress:
- A **summary statistics panel** to dynamically display top predictors (e.g., highest-rated genres) is not yet fully operational.
- A **map chart** to show the distribution of anime viewers across different regions or a **line chart** to illustrate the trend of anime popularity over time. We’ve yet to decide between these options and implement them.
- The **Studio** filter is not yet implemented.

## Strengths of the Current Dashboard
The prototype excels in several areas:
- The heat map quickly reveals correlations between predictors, simplifying the analysis of success factors.
- The bar chart provides clear, actionable data on genre performance, supporting content planning.
- The time-series plot’s slider enables effective seasonal trend analysis, crucial for release strategies.
- The radar chart offers a multi-dimensional view of performance metrics, facilitating comparisons.

## Limitations
There are some notable drawbacks:
- The incomplete summary statistics panel limits dynamic insights into top predictors.
- The potential map chart cannot currently link with other visualizations due to differences in the dataset, restricting integrated analysis.
- The line chart for popularity trends has not been finalized or created, leaving some popularity insights unexplored.
- The dynamic change causing by filter among visualizations is not properly implemented. (work but not good)

## Future Improvements
To enhance the dashboard, we plan to:
- Finalize the summary statistics panel to dynamically highlight top predictors.
- Choose between the map chart or line chart and implement the selected option for additional insights.
- Strengthen filter integration across all visualizations for a seamless user experience.
- Address minor issues like occasional filter update failures and radar chart misalignments.

In summary, our prototype effectively identifies key drivers of anime success but requires further refinement. Completing the pending features and resolving limitations will make it a robust, user-friendly tool for anime companies, studios, and investors.