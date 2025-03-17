# Reflection for Milestone 4

For Milestone 4, we’ve refined our "Anime Popularity & Ratings Dashboard" based on the requirements and feedback received. The enhancements focus on improving interactivity, visualization clarity, and feature completeness to better assist anime companies, studios, and investors in identifying key success factors.

## Received Feedback
- **Performance & Usability**

    One of the most consistent concerns is the slow loading time of the dashboard. Users reported long wait times without knowing whether the dashboard was functioning correctly. Some suggested displaying a loading indicator with an estimated wait time (e.g., “Please wait up to 5 seconds”). Additionally, making the dashboard more compatible with different computing capabilities would improve accessibility.

- **Design & Readability**

    Users mentioned a lack of dashboard and chart titles, which made it difficult to interpret the data. A title banner for the dashboard, along with clear labels for each visualization, would help in understanding the presented information.

    Although the color theme was praised, users pointed out inconsistencies in color usage across different charts. Ensuring a coordinated color palette, font styles, and sizes would enhance the visual coherence of the dashboard.

- **Functionality & Interactivity**

    Several users suggested improving filter functionality. Allowing multi-select filters for categories like genres and show types would provide more flexibility. Additionally, relocating the filter section (e.g., to the top-left or top-right) could improve accessibility.


## **Ease of Use and Recurring Feedback Themes**
User and TA feedback has helped us refine the dashboard significantly. Users generally found the dashboard visually appealing but encountered challenges with:
    
1. **Performance** – Long load times and occasional lag when updating filters.

2. **Readability** – Lack of a clear title for the dashboard and missing labels on certain charts.

3. **Interactivity** – The need for multi-select filters and clearer filter placement.

A common theme in feedback was that while individual charts were insightful, their integration into a seamless, interactive experience needed improvement.

## **Most Valuable Insights from Feedback**
One of the most useful insights was **the importance of a clear, well-structured user experience**. The feedback highlighted the necessity of **consistent color schemes, proper titles, and well-placed filters** to enhance clarity. Additionally, concerns about **load times and screen adaptability** reinforced the need to optimize performance.

In retrospect, these insights have shaped our priorities, pushing us to focus on **responsiveness, usability, and interactive coherence** rather than adding more features. Moving forward, addressing these feedback points will be crucial for ensuring a smooth user experience.


## Implemented Features
The dashboard currently includes:

- A **heat map** showing correlations between predictors and outcomes (popularity, ratings). It’s the core visualization, highlighting key influences in different categories predictors(e.g., genre, type, studio).

- A **bar chart** displaying average ratings by genre, offering clear insights into genre performance.

- A **time-series plot** with a slider filter, allowing users to explore trends over time and identify optimal release windows.

- A **radar chart** comparing multiple metrics (e.g., number of completed, dropped, score) across genres or studios or anime types.

- A **Map plot**: Shows the geographical distribution of anime popularity and viewer demographics.

- **Filters** for genres, types, and studios, linked to the bar chart, time-series plot, heat map, and radar chart for basic interactivity.

## Improvements
Based on user feedback, we have made several enhancements to existing features:
- **Responsiveness**: Improved the dashboard's response time, ensuring smoother interactions and quicker updates when filters are applied.
- **Visual Consistency**: Applied a unified color theme and clear titles across all visualizations to enhance readability and aesthetic appeal.
- **Heat Map**: Refined to highlight key influences more effectively, with a consistent color theme and clear title.
- **Bar Chart**: Enhanced with a distinct title and unified color scheme for easier interpretation of genre performance.
- **Time-Series Plot**: Equipped with a slider filter and improved visual appeal through a consistent color theme.
- **Radar Chart**: Redesigned for quicker comparisons with a clear title and cohesive color theme.
- **Filters**: Improved with clear labels and better integration across all visualizations, enhancing interactivity and user understanding.

These improvements ensure a more user-friendly and visually appealing dashboard, better meeting the needs of anime companies, studios, and investors.


We have significantly improved responsiveness, visual clarity, and interactivity based on feedback. The dashboard now features consistent color schemes, clear titles, and improved filters. The heat map, bar chart, time-series plot, and radar chart have been enhanced for readability, and filters now allow better multi-selection and integration across visualizations.

However, some areas still need refinement. The loading time remains a concern, and while we have optimized it, further improvements may be required. Additionally, filter interactions are sometimes inconsistent, which will need further debugging. Future iterations could focus on these issues while ensuring continued usability improvements.





