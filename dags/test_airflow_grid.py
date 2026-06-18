from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'kenan',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'airflow_grid_test',
    default_args=default_args,
    description='Testing our data engineering lab environment',
    schedule_interval=None,
    catchup=False,
) as dag:

    task_welcome = BashOperator(
        task_id='welcome_message',
        bash_command='echo "Welcome Kenan to Apache Airflow!"',
    )

    task_ping_kafka = BashOperator(
        task_id='check_kafka_network',
        bash_command='echo "Testing grid connections..."',
    )

    task_welcome >> task_ping_kafka