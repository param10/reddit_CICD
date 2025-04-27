from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum  
from reddit_ETL import run_ETL

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,  # ← should be boolean, not string 'false'
    'start_date': pendulum.now().subtract(days=1),  # ← pendulum instead of hardcoding
    'email': ['parambytes@gmail.com'],  # ← needs to be inside a list []
    'email_on_failure': False,  # ← boolean, not string
    'email_on_retry': False,  # ← boolean, not string
    'retries': 1,  # ← typo! You had 'retires', correct is 'retries'
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'reddit_dag',
    default_args=default_args,
    description='Basic ETL practice',
    schedule=None,  # optional: no auto-run
    catchup=False  # optional: do not run missed DAG runs
)

run_etl_task = PythonOperator(
    task_id='complete_reddit_etl',
    python_callable=run_ETL,  # ← typo fixed: 'python_callable' not 'python_callabale'
    dag=dag
)

run_etl_task
