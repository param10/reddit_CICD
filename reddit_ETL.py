import praw
import pandas as pd
import datetime as datetime

def run_ETL():
    print("🔵 Starting ETL Process...")

    auth = praw.Reddit(
        client_id="iWOaXhCh7BCDyDgoyyjHpw",
        client_secret="Vs52KpN5pNg-nAaUj3aZJ04-AjKBUw",
        user_agent="just implementation of airflow."
    )

    posts_data = []
    subread = auth.subreddit('learnprogramming')

#testing

    for submission in subread.search(
        query='python',
        limit=100,
        sort='top',
        time_filter='year',
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

    print(f"🔵 Fetched {len(posts_data)} posts.")

    if len(posts_data) == 0:
        print("⚠️ No posts found. ETL process finished early.")
        return

    df = pd.DataFrame(posts_data)

    try:
        print("🔵 Attempting to save to S3...")
        df.to_csv(
            "s3://reddit-dag-paramjaswal/reddit_posts.csv",
            index=False,
            storage_options={"key": auth._core._authorizer._client_id, "secret": auth._core._authorizer._client_secret}
        )
        print("✅ Successfully uploaded to S3.")
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")

    print("🟢 ETL Process Completed.")


if __name__ == "__main__":
    run_ETL()

