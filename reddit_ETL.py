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

    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Save locally
    local_filename = f'reddit_posts_{today_str}.csv'
    df.to_csv(local_filename, index=False)
    print(f"🔵 Data saved locally as {local_filename}")

    # Save to S3
    try:
        print("🔵 Attempting to save to S3...")
        s3_filename = f"s3://reddit-dag-paramjaswal/reddit_posts_{today_str}.csv"
        df.to_csv(s3_filename, index=False)
        print(f"✅ Successfully uploaded to S3 as {s3_filename}")
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")

    print("🟢 ETL Process Completed.")

if __name__ == "__main__":
    run_ETL()
