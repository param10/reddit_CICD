from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
from reddit_ETL import run_ETL

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': pendulum.now().subtract(days=1),
    'email': ['parambytes@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'reddit_dag',
    default_args=default_args,
    description='Basic ETL practice',
    schedule_interval=None,
    catchup=False
)

run_etl_task = PythonOperator(
    task_id='complete_reddit_etl',
    python_callable=run_ETL,
    dag=dag
)

run_etl_task
