# Anime Popularity & Ratings Dashboard
## Overview
This project aims to develop an interactive dashboard that analyzes key factors affecting anime popularity and ratings. The primary goal is to provide actionable insights for anime companies, studios, and investors to maximize profitability by identifying the most critical predictors influencing anime success.

## Problem Statement
The anime industry is a competitive market where companies must decide on optimal production strategies. Questions such as:
- **"What factors contribute most to high ratings?"** 
- **"Which genres have the highest audience retention?"** 
- **"When is the best time to release anime for maximum viewership?"** 
These are essential for stakeholders. Our dashboard will help answer these questions using data-driven insights.

## Application Interface & Features
The app will consist of multiple interactive visualization panels, allowing users to explore different aspects of anime ratings and popularity. The interface will be designed with ease of navigation in mind, ensuring that stakeholders can quickly derive insights.

### **Main Components**

1. **Landing Page (Overview & Summary Metrics)**
   - Displays total number of anime in the dataset.
   - Shows key summary statistics (e.g., average rating, most popular genre, most successful studios).
   - Allows users to filter anime by genre, studio, release year, or type.

2. **Main Visualization Panel (Key Predictor for Ratings)**
   - A bar chart or correlation heatmap showing **the strongest predictor influencing anime ratings**.
   - This will be the primary insight guiding decisions on anime production.

3. **Supporting Visualization Panels**
   - **Correlation between important predictors and target varaible (Heat Map)**
     - Identifies the most important predictors for anime ratings and popularity.
   - **Best Time to Publish Anime (Time-Series Plot)**
     - Identifies the optimal time of year for anime releases based on historical trends.
   - **Completion vs. Drop Rate by Genre (Stacked Bar Chart)**
     - Shows audience retention for different anime genres.
   - **Impact of Studio, Producer & Source Material on Ratings (Grouped Bar Chart)**
     - Analyzes the effect of production decisions on anime success.
   - **Effect of Type & Duration on Ratings (Box Plot/Violin Plot)**
     - Evaluates how format (TV, Movie, OVA) and duration influence ratings.
   - **Episode Length vs. Ratings (Scatter Plot)**
     - Determines whether longer or shorter series tend to perform better.

4. **Final Summary Panel**
   - Presents a ranked list of the most significant predictors of anime success.
   - Includes recommendations for maximizing profitability based on the analysis.

## User Interaction
- Users can filter results based on **Type, Genres, Studio**.
- Hovering over graphs provides detailed data points for deeper analysis.
- Adjusting and dragging the slider on the bottom of the page for time filtering.

## Sketch of App Layout
![Dashboard Sketch](link_to_sketch_image)

This dashboard will serve as a valuable decision-making tool for anime production and investment strategy, ensuring that target audiences can leverage **data-driven insights** to create successful and profitable anime productions.

## Project Setup
```
pip install -r requirements.txt
```


<div style="display: flex; flex-direction: column; align-items: center;">
  <h6>The dataset is collected from:</h6>
  <a href="https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset" target="_blank">
  <img src="./assets/others/Kaggle.png" alt="kaggle site logo" width="50" height="25">
  </a>
</div>
