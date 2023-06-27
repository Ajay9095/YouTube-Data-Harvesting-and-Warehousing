import streamlit as st
import sqlalchemy
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import plotly.express as px
from pymongo import MongoClient
from bson import ObjectId
import requests
import json
from streamlit_lottie import st_lottie

mysql_host = 'localhost'
mysql_user = 'root'
mysql_port = 3306
mysql_password = 'ajaykumar_A04'
mysql_database = 'youtube_sql'

engine = sqlalchemy.create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}')

def get_table_data(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

channel_data = get_table_data("channel_table")

video_data = get_table_data("video_table")

comment_data = get_table_data("comment_table")

with st.sidebar:
    selected = option_menu(
    menu_title = "Youtube",
    options = ["Home", "Data Analysis", "Data files", "Data Queries", "Search Queries"],
    icons = ["house", "youtube", "files", "map", "search"],
    default_index=0,
)

#-------------------------------------------------------Home-----------------------------------------------------------#

if selected == "Home":

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
    lottie_visualization = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_frJ5A7.json")

    st_lottie(lottie_visualization)

    st.title("Intro")

    st.image("youtube.jpg")
    "____"

    st.header("YouTube Data Harvesting and Warehousing")
    "____"

    st.write("YouTube Data Harvesting and Warehousing involves collecting and storing data related to YouTube channels, videos, comments, likes-dislikes, duration, and subscription count. This process provides valuable insights into user behavior, content performance, and audience preferences on the platform. Harvesting data from YouTube channels includes information about channel owners, subscriber counts, and statistics, offering insights into their popularity and growth. Collecting data on videos enables the analysis of metrics such as view counts, likes-dislikes, and video durations, helping evaluate user engagement and sentiment. Comments on YouTube videos are harvested to analyze user feedback, sentiment, and engagement levels. Duration data provides insights into video lengths, aiding content creators and advertisers in understanding user preferences. Subscription count data offers information on channel popularity and potential reach, assisting in tracking trends and measuring audience loyalty. By leveraging YouTube data harvesting and warehousing, content creators, marketers, and researchers can make data-driven decisions, optimize strategies, and enhance user engagement, ultimately catering to their target audience more effectively.")
    "____"

#------------------------------------------------------END-------------------------------------------------------------#



#--------------------------------------------------Data Analysis-------------------------------------------------------#

if selected == "Data Analysis":

    st.title("Welcome to Youtube Warehouse")
    
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
    lottie_visualization = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_idkdzvv1.json")
    lottie_button = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_EAfMOs/Youtube.json")

    col1, col2 = st.columns(2)

    with col1:
        st_lottie(lottie_visualization, width=450, height=450)

    with col2:
        st_lottie(lottie_button, width=450, height=450)

    selected_table = st.selectbox("Select a table", ("channel_table", "video_table", "comment_table"))

    if selected_table == "channel_table":
        st.title("Channel Table")
        colormap = 'coolwarm'  
        styled_df = channel_data.style.background_gradient(cmap=colormap)
        st.dataframe(styled_df)
        if st.button("Download Channel Data"):
            st.write("Downloading channel_data.csv...")
            channel_data.to_csv("channel_data.csv", index=False)
            st.success("Download completed!")

    elif selected_table == "video_table":
        st.title("Video Table")
        st.dataframe(video_data)
        if st.button("Download Video Data"):
            st.write("Downloading video_data.csv...")
            video_data.to_csv("video_data.csv", index=False)
            st.success("Download completed!")

    elif selected_table == "comment_table":
        st.title("Comment Table")
        st.dataframe(comment_data)
        if st.button("Download comment Data"):
            st.write("Downloading comment_data.csv...")
            comment_data.to_csv("comment_data.csv", index=False)
            st.success("Download completed!")
        
    if selected_table == "channel_table":
        st.header("Data Analysis")
        st.subheader("Subscription Count per Channel")
        fig = px.bar(channel_data, x="Channel_Name", y="Subscription_Count")
        st.plotly_chart(fig)

    elif selected_table == "video_table":
        st.header("Data Analysis")
        st.subheader("Video Views Distribution by Channel")
        fig = px.pie(video_data, values="View_Count", names="Channel_Name")
        st.plotly_chart(fig)

#-------------------------------------------------------END-----------------------------------------------------------#




#-----------------------------------------------------Data files------------------------------------------------------#

if selected == "Data files":

    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            return super().default(o)

    mongo_host = 'localhost'
    mongo_port = 27017
    mongo_database = 'Youtube'
    mongo_collection = 'youtube_warehousing'

    client = MongoClient(mongo_host, mongo_port)

    db = client[mongo_database]
    collection = db[mongo_collection]

    data = collection.find()

    data_list = list(data)

    st.title("MongoDB Collection Data:")
    "_____"

    if st.button("Download Data as JSON"):
        with open("mongo_data.json", "w") as f:
            json.dump(data_list, f, cls=JSONEncoder)

        st.success("Download the JSON file:")
        st.download_button(label="Download", data="mongo_data.json", file_name="mongo_data.json", mime="application/json")

    for item in data_list:
        st.json(item)

#---------------------------------------------------------END---------------------------------------------------------#



#-----------------------------------------------------Data Queries----------------------------------------------------#

if selected == "Data Queries":

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
    lottie_visualization = load_lottieurl("https://assets5.lottiefiles.com/private_files/lf30_w11f2rwn.json")
    st_lottie(lottie_visualization)

    channel_names = [
    'Bayya Sunny Yadav',
    'The Fashion Verge',
    'Aye Jude',
    'JerryRigEverything',
    'AcademicEnglishHelp',
    'Apna College',
    'Prasadtechintelugu',
    'Harsha Sai - For You Telugu',
    'India Today',
    'Fit Tuber'
    ]

    df = pd.DataFrame(channel_names, columns=['Channel Names'])

    st.table(df)

    st.write("-----------------------Copy the above Channel Name and Paste below in the box and press enter------------------")
    "_____"

    def get_channel_data(channel_name):
        query = f"SELECT * FROM channel_table WHERE Channel_Name = '{channel_name}'"
        df = pd.read_sql(query, engine)
        return df

    def get_video_data(channel_name):
        query = f"SELECT * FROM video_table WHERE Channel_Name = '{channel_name}'"
        df = pd.read_sql(query, engine)
        return df

    def get_comment_data(channel_name):
        query = f"SELECT * FROM comment_table WHERE Channel_Name = '{channel_name}'"
        df = pd.read_sql(query, engine)
        return df

    channel_name = st.text_input("Enter the channel name:")

    channel_data = get_channel_data(channel_name)

    video_data = get_video_data(channel_name)

    comment_data = get_comment_data(channel_name)

    st.header("Channel Data")
    if not channel_data.empty:
        st.dataframe(channel_data)
    else:
        st.write("No data found for the given channel name.")

    st.header("Video Data")
    if not video_data.empty:
        st.dataframe(video_data)
    else:
        st.write("No data found for the given channel name.")

    st.header("Comment Data")
    if not comment_data.empty:
        st.dataframe(comment_data)
    else:
        st.write("No data found for the given channel name.")

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
    lottie_visualization = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_g63n5jcl.json")
    st_lottie(lottie_visualization)

#-------------------------------------------------------END-----------------------------------------------------------#



#--------------------------------------------------Search Queries-----------------------------------------------------#
if selected == "Search Queries":

    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
    lottie_visualization = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_ugedlis6.json")

    st_lottie(lottie_visualization)

    def retrieve_data_from_mysql(query):
        with mydb.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
        return df

    # Query: Total number of views for each channel and their corresponding channel names
    query1 = '''
    SELECT channel_table.Channel_Name, SUM(video_table.View_Count) AS Total_Views
    FROM channel_table
    INNER JOIN video_table ON channel_table.Channel_Id = video_table.Channel_Id
    GROUP BY channel_table.Channel_Name
    '''

    # Query: Channels with the most number of videos and the count of videos
    query2 = '''
    SELECT channel_table.Channel_Name, COUNT(video_table.Video_Id) AS Video_Count
    FROM channel_table
    INNER JOIN video_table ON channel_table.Channel_Id = video_table.Channel_Id
    GROUP BY channel_table.Channel_Name
    ORDER BY Video_Count DESC
    '''

    # Query: Top 10 most viewed videos and their respective channels
    query3 = '''
    SELECT video_table.Video_Name, channel_table.Channel_Name, video_table.View_Count
    FROM video_table
    INNER JOIN channel_table ON video_table.Channel_Id = channel_table.Channel_Id
    ORDER BY video_table.View_Count DESC
    LIMIT 10
    '''

    # Query: Number of comments on each video and their corresponding video names
    query4 = '''
    SELECT video_table.Video_Name, COUNT(comment_table.Comment_Id) AS Comment_Count
    FROM video_table
    LEFT JOIN comment_table ON video_table.Video_Id = comment_table.Video_Id
    GROUP BY video_table.Video_Name
    '''

    # Query: Videos with the highest number of likes and their corresponding channel names
    query5 = '''
    SELECT video_table.Video_Name, channel_table.Channel_Name, video_table.Like_Count
    FROM video_table
    INNER JOIN channel_table ON video_table.Channel_Id = channel_table.Channel_Id
    ORDER BY video_table.Like_Count DESC
    '''

    # Query: Total number of likes and dislikes for each video and their corresponding video names
    query6 = '''
    SELECT video_table.Video_Name, SUM(video_table.Like_Count) AS Total_Likes, SUM(video_table.Dislike_Count) AS Total_Dislikes
    FROM video_table
    GROUP BY video_table.Video_Name
    '''
    # Query: Names of all videos and their corresponding channels
    query7 = '''
    SELECT video_table.Video_Name, channel_table.Channel_Name
    FROM video_table
    INNER JOIN channel_table ON video_table.Channel_Id = channel_table.Channel_Id
    '''

    # Retrieve the data from MySQL
    df1 = retrieve_data_from_mysql(query1)
    df2 = retrieve_data_from_mysql(query2)
    df3 = retrieve_data_from_mysql(query3)
    df4 = retrieve_data_from_mysql(query4)
    df5 = retrieve_data_from_mysql(query5)
    df6 = retrieve_data_from_mysql(query6)
    df7 = retrieve_data_from_mysql(query7)

    with st.expander("Total number of views for each channel and their corresponding channel names"):
        st.dataframe(df1)
        fig, ax = plt.subplots()
        ax.pie(df1['Total_Views'], labels=df1['Channel_Name'], autopct='%1.1f%%')
        ax.set_aspect('equal')
        st.pyplot(fig)

    with st.expander("Channels with the most number of videos and the count of videos"):
        st.dataframe(df2)
        
    with st.expander("Top 10 most viewed videos and their respective channels"):
        st.dataframe(df3)
        fig, ax = plt.subplots()
        ax.pie(df3['View_Count'], labels=df3['Channel_Name'], autopct='%1.1f%%')
        ax.set_aspect('equal')
        st.pyplot(fig)

    with st.expander("Number of comments on each video and their corresponding video names"):
        st.dataframe(df4)

    with st.expander("Videos with the highest number of likes and their corresponding channel names"):
        st.dataframe(df5)
        fig, ax = plt.subplots()
        ax.pie(df5['Like_Count'], labels=df5['Channel_Name'], autopct='%1.1f%%')
        ax.set_aspect('equal')
        st.pyplot(fig)

    with st.expander("Total number of likes and dislikes for each video and their corresponding video names"):
        st.dataframe(df6)

    with st.expander("Names of all videos and their corresponding channels"):
        st.dataframe(df7)

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
    lottie_visualization = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_df7psn7k.json")
    "___"
    st_lottie(lottie_visualization)

#-------------------------------------------------------END-----------------------------------------------------------#



from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Youtube']
collection = db['youtube_warehousing']

from googleapiclient.discovery import build

def youtube_api_request(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    channel_request = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        id=channel_id
    )
    channel_response = channel_request.execute()
    channel = channel_response['items'][0]

    channel_obj = {
        "Channel_Name": channel['snippet']['title'],
        "Channel_Id": channel_id,
        "Subscription_Count": int(channel['statistics']['subscriberCount']),
        "Channel_Views": int(channel['statistics']['viewCount']),
        "Channel_Description": channel['snippet']['description'],
        "Playlist_Id": channel.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads', '')
    }

    video_request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=5  
    )
    video_response = video_request.execute()
    videos = video_response['items']

    response = {
        "Channel_Name": channel_obj
    }

    for video in videos:
        video_id = video['id']['videoId']
        video_details_request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        )
        video_details_response = video_details_request.execute()
        video_details = video_details_response['items'][0]

        video_obj = {
            "Video_Id": video_id,
            "Video_Name": video_details['snippet']['title'],
            "Video_Description": video_details['snippet']['description'],
            "Tags": video_details['snippet'].get('tags', []),
            "PublishedAt": video_details['snippet']['publishedAt'],
            "View_Count": int(video_details['statistics']['viewCount']),
            "Like_Count": int(video_details['statistics'].get('likeCount', 0)),
            "Dislike_Count": int(video_details['statistics'].get('dislikeCount', 0)),
            "Favorite_Count": int(video_details['statistics'].get('favoriteCount', 0)),
            "Comment_Count": int(video_details['statistics'].get('commentCount', 0)),
            "Duration": video_details['contentDetails'].get('duration', 'N/A'),
            "Thumbnail": video_details['snippet']['thumbnails']['default']['url'],
            "Caption_Status": video_details['contentDetails'].get('caption', 'N/A'),
            "Comments": {}
        }

        comments_request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=5  
        )
        comments_response = comments_request.execute()
        comments = comments_response['items']

        for i, comment in enumerate(comments):
            comment_obj = {
                "Comment_Id": comment['id'],
                "Comment_Text": comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                "Comment_Author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                "Comment_PublishedAt": comment['snippet']['topLevelComment']['snippet']['publishedAt']
            }
            video_obj['Comments']['Comment_Id_' + str(i+1)] = comment_obj

        response["Video_Id_" + str(len(response) - 1)] = video_obj

    return response

api_key = 'AIzaSyDvtX9sU9nfSoW5BG2_xgzPvFO-5Ih6a8I'
channel_id = 'UCYC6Vcczj8v-Y5OgpEJTFBw'
response = youtube_api_request(api_key, channel_id)

import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="@jaykumar_A04", database="youtube_sql")

cursor = mydb.cursor()

import pymysql

def create_mysql_tables(mysql_host, mysql_user, mysql_password, mysql_database):
    
    mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)

    with mysql_conn.cursor() as cursor:
        create_channel_table_sql = """
        CREATE TABLE IF NOT EXISTS channel_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Channel_Name VARCHAR(255),
            Channel_Id VARCHAR(255),
            Subscription_Count INT,
            Channel_Views BIGINT,
            Channel_Description TEXT,
            Playlist_Id VARCHAR(255)
        )
        """
        cursor.execute(create_channel_table_sql)

    with mysql_conn.cursor() as cursor:
        create_video_table_sql = """
        CREATE TABLE IF NOT EXISTS video_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Channel_Name VARCHAR(255),
            Channel_Id VARCHAR(255),
            Video_Id VARCHAR(255),
            Video_Name VARCHAR(255),
            Video_Description TEXT,
            PublishedAt DATETIME,
            View_Count INT,
            Like_Count INT,
            Dislike_Count INT,
            Favorite_Count INT,
            Comment_Count INT,
            Duration VARCHAR(255),
            Thumbnail VARCHAR(255),
            Caption_Status VARCHAR(255)
        )
        """
        cursor.execute(create_video_table_sql)
        
    with mysql_conn.cursor() as cursor:
        create_comment_table_sql = """
        CREATE TABLE IF NOT EXISTS comment_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Channel_Name VARCHAR(255),
            Channel_Id VARCHAR(255),
            Comment_Id VARCHAR(255),
            Comment_Text TEXT,
            Comment_Author VARCHAR(255),
            Comment_PublishedAt DATETIME,
            Video_Id VARCHAR(255)
        )
        """
        cursor.execute(create_comment_table_sql)

    mysql_conn.commit()
    mysql_conn.close()

mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'ajaykumar_A04'
mysql_database = 'youtube_sql'

create_mysql_tables(mysql_host, mysql_user, mysql_password, mysql_database)

import pymongo
import pymysql
from datetime import datetime

def convert_iso8601_to_mysql_datetime(iso8601_datetime):
    # Convert ISO 8601 datetime to MySQL datetime format
    dt = datetime.strptime(iso8601_datetime, '%Y-%m-%dT%H:%M:%SZ')
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def migrate_data_from_mongodb_to_mysql(mongo_uri, mongodb_database, mongodb_collection,
                                      mysql_host, mysql_user, mysql_password, mysql_database):
    # Connect to MongoDB
    mongo_client = pymongo.MongoClient(mongo_uri)
    mongo_db = mongo_client[mongodb_database]
    mongo_collection = mongo_db[mongodb_collection]

    mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)

    data = list(mongo_collection.find())
    
    for channel_data in data:
        channel_name = channel_data.get('Channel_Name', {}).get('Channel_Name', '')
        channel_id = channel_data.get('Channel_Name', {}).get('Channel_Id', " ")
        subscription_count = channel_data.get('Channel_Name', {}).get('Subscription_Count', 0)
        channel_views = channel_data.get('Channel_Name', {}).get('Channel_Views', 0)
        channel_description = channel_data.get('Channel_Name', {}).get('Channel_Description', "")
        playlist_id = channel_data.get('Channel_Name', {}).get('Playlist_Id', '')

        with mysql_conn.cursor() as cursor:
            sql = "INSERT INTO channel_table (Channel_Name, Channel_Id, Subscription_Count, Channel_Views, Channel_Description, Playlist_Id) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (channel_name, channel_id, subscription_count, channel_views, channel_description, playlist_id)
            cursor.execute(sql, values)
        mysql_conn.commit()
    
    
    for video_data in data:
        channel_name = video_data.get('Channel_Name', {}).get('Channel_Name', '')
        channel_id = video_data.get('Channel_Name', {}).get('Channel_Id', " ")
        video_id = video_data.get('Video_Id_0', {}).get('Video_Id', '')
        video_name = video_data.get('Video_Id_0', {}).get('Video_Name', '')
        video_description = video_data.get('Video_Id_0', {}).get('Video_Description', '')
        published_at = video_data.get('Video_Id_0', {}).get('PublishedAt', '')
        view_count = video_data.get('Video_Id_0', {}).get('View_Count', 0)
        like_count = video_data.get('Video_Id_0', {}).get('Like_Count', 0)
        dislike_count = video_data.get('Video_Id_0', {}).get('Dislike_Count', 0)
        favorite_count = video_data.get('Video_Id_0', {}).get('Favorite_Count', 0)
        comment_count = video_data.get('Video_Id_0', {}).get('Comment_Count', 0)
        duration = video_data.get('Video_Id_0', {}).get('Duration', '')
        thumbnail = video_data.get('Video_Id_0', {}).get('Thumbnail', '')
        caption_status = video_data.get('Video_Id_0', {}).get('Caption_Status', '')

        published_at = convert_iso8601_to_mysql_datetime(published_at)
        
        with mysql_conn.cursor() as cursor:
            sql = "INSERT INTO video_table (Channel_Name, Channel_Id, Video_Id, Video_Name, Video_Description, PublishedAt, View_Count, Like_Count, Dislike_Count, Favorite_Count, Comment_Count, Duration, Thumbnail, Caption_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (channel_name, channel_id, video_id, video_name, video_description, published_at, view_count, like_count, dislike_count, favorite_count, comment_count, duration, thumbnail, caption_status)
            cursor.execute(sql, values)
        mysql_conn.commit()
                
    mongo_client.close()
    mysql_conn.close()

mongo_uri = 'mongodb://localhost:27017'
mongodb_database = 'Youtube'
mongodb_collection = 'youtube_warehousing'
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'ajaykumar_A04'
mysql_database = 'youtube_sql'

migrate_data_from_mongodb_to_mysql(mongo_uri, mongodb_database, mongodb_collection,
                                  mysql_host, mysql_user, mysql_password, mysql_database)


import pymongo
import pymysql
from datetime import datetime

def convert_iso8601_to_mysql_datetime(iso8601_datetime):
    if iso8601_datetime:
        try:
            dt = datetime.strptime(iso8601_datetime, '%Y-%m-%dT%H:%M:%SZ')
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
    else:
        return None

def migrate_comments_from_mongodb_to_mysql(mongo_uri, mongodb_database, mongodb_collection,
                                          mysql_host, mysql_user, mysql_password, mysql_database):
    
    mongo_client = pymongo.MongoClient(mongo_uri)
    mongo_db = mongo_client[mongodb_database]
    mongo_collection = mongo_db[mongodb_collection]

    mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)

    data = list(mongo_collection.find())

    for video_data in data:
        channel_name = video_data.get('Channel_Name', {}).get('Channel_Name', '')
        channel_id = video_data.get('Channel_Name', {}).get('Channel_Id', '')

        video_id = video_data.get('Video_Id_0', {}).get('Video_Id', '')

        comments = video_data.get('Video_Id_0', {}).get('Comments', {})
        if comments:
            for comment_id, comment_data in comments.items():
                comment_text = comment_data.get('Comment_Text', '')
                comment_author = comment_data.get('Comment_Author', '')
                comment_published_at = comment_data.get('Comment_PublishedAt', '')

                comment_published_at = convert_iso8601_to_mysql_datetime(comment_published_at)

                with mysql_conn.cursor() as cursor:
                    sql = "INSERT INTO comment_table (Channel_Name, Channel_Id, Comment_Id, Comment_Text, Comment_Author, Comment_PublishedAt, Video_Id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    values = (channel_name, channel_id, comment_id, comment_text, comment_author, comment_published_at, video_id)
                    cursor.execute(sql, values)
                mysql_conn.commit()

    mongo_client.close()
    mysql_conn.close()

mongo_uri = 'mongodb://localhost:27017'
mongodb_database = 'Youtube'
mongodb_collection = 'youtube_warehousing'
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'ajaykumar_A04'
mysql_database = 'youtube_sql'

migrate_comments_from_mongodb_to_mysql(mongo_uri, mongodb_database, mongodb_collection,
                                       mysql_host, mysql_user, mysql_password, mysql_database)
