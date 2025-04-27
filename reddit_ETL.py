import praw
import pandas as pd
import json
import datetime as datetime
import s3fs
from dotenv import load_dotenv
import os


def run_ETL():


    auth = praw.Reddit(
        client_id = "iWOaXhCh7BCDyDgoyyjHpw",
        client_secret = "Vs52KpN5pNg-nAaUj3aZJ04-AjKBUw",
        user_agent = "jsut implementation of airflow."
    )

    # print(auth.user.me())

    posts_data = []

    subread = auth.subreddit('learnprogramming')

    for submission in subread.search(
        query = 'python',
        limit = 100,
        sort = 'top',
        time_filter = 'year',
        params={"restrict_sr": "true"}
    ):
        posts_data.append({
            "title": submission.title,
            "selftext": submission.selftext,
            "author": str(submission.author),  
            "score": submission.score,
            "num_comments": submission.num_comments,
            "created_utc": datetime.datetime.fromtimestamp(submission.created_utc, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            "url": submission.url
        })

    df = pd.DataFrame(posts_data)

    load_dotenv()
    AWS_ACCESS_KEY = os.getenv("KEY")
    AWS_SECRET_KEY = os.getenv("SECRET_KEY")

    df.to_csv("s3://reddit-dag-paramjaswal/reddit_posts.csv", index=False, storage_options={"key": "", "secret": ""})







