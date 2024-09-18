from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

default_args = {
    'owner': 'Seif Yasser airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}


def run_etl_script():
    script_path = "/opt/airflow/elt/etl_script.py"
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


dag = DAG(
    dag_id='elt_and_dbt',
    default_args=default_args,
    description="an ElT workflow with dbt",
    start_date=datetime(2024, 9, 11),
    catchup=False
)

t1 = PythonOperator(
    task_id="run_elt_script",
    python_callable=run_etl_script,
    dag=dag
)

t2 = DockerOperator(
    task_id="dbt_run",
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt"
    ],
    auto_remove="success",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(source='E:/new_seef/flash seef/Data engineer/projects/elt/elt/custom_postgres',
              target='/dbt', type='bind'),
        Mount(source='C:/Users/Dell/.dbt',
              target='/root', type='bind')
    ],
    dag=dag
)

t1 >> t2
