# YouTube Data Harvesting and Warehousing

This repository contains a Streamlit application for analyzing YouTube data. The application allows users to explore and visualize data related to YouTube channels, videos, and comments. It provides insights into user behavior, content performance, and audience preferences on the platform.

## Deployment of "Streamlit app" using Visual Studio Code.
https://github.com/Ajay9095/YouTube-Data-Harvesting-and-Warehousing/assets/122981534/59b28934-16f9-43b2-a214-3a6964d45510

## Dependencies

The following dependencies are required to run the application:

- streamlit
- sqlalchemy
- streamlit_option_menu
- pandas
- mysql.connector
- matplotlib
- plotly.express
- pymongo
- bson
- requests
- json
- streamlit_lottie

You can install the dependencies by running the following command:

```bash
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```bash
streamlit run app.py
```

The application will launch in your browser, and you can interact with it to explore and analyze YouTube data.

## Functionality

The application provides the following functionality:

### Home

- Displays an introduction to YouTube Data Harvesting and Warehousing.
- Shows an animation and an image related to YouTube.
- Provides information about the process of collecting and storing YouTube data.
- Offers insights into the benefits of leveraging YouTube data for decision-making.

### Data Analysis

- Allows users to select a table (channel_table, video_table, or comment_table) to analyze.
- Displays the selected table's data in a DataFrame format.
- Provides options to download the data as a CSV file.
- Offers data visualizations based on the selected table.

### Data Files

- Connects to a MongoDB database and retrieves data from the "youtube_warehousing" collection.
- Displays the retrieved data in a JSON format.
- Provides an option to download the data as a JSON file.

### Data Queries

- Allows users to enter a channel name and retrieve data related to that channel from the MySQL database.
- Displays the retrieved channel data, video data, and comment data in separate tables.
- Provides an animation related to data queries.

### Search Queries

- Executes predefined SQL queries to retrieve data from the MySQL database.
- Displays the retrieved data in DataFrame format.
- Provides data visualizations based on the retrieved data.
