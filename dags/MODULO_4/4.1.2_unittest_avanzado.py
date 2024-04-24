# airflow_project/dags/my_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests

def fetch_data():
    response = requests.get("https://api.example.com/data")
    if response.status_code != 200:
        raise Exception("API request failed")
    return response.json()

def process_data(ti):
    raw_data = ti.xcom_pull(task_ids='fetch_data')
    processed_data = [process_record(record) for record in raw_data]
    return processed_data

def load_data(ti):
    data_to_load = ti.xcom_pull(task_ids='process_data')
    print(f"Loading {len(data_to_load)} records into the database...")

default_args = {
    'owner': 'Docente',
    'start_date': datetime(2022, 1, 1),
    'retry_delay': timedelta(minutes=5),
    'retries': 2
}

dag = DAG(
    dag_id='example_advanced_unittest',
    default_args=default_args,
    schedule_interval='@daily'
)

with dag:
    fetch_task = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data
    )

    process_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    fetch_task >> process_task >> load_task