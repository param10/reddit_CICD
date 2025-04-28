import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from reddit_ETL import run_ETL

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 27),
    'retries': 1,
}

with DAG(
    dag_id='reddit_dag',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['reddit'],
) as dag:
    
    reddit_etl_task = PythonOperator(
        task_id='run_reddit_etl',
        python_callable=run_ETL,
    )
