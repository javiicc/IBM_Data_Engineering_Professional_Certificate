import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch, helpers


default_args = {
    'owner': 'javier',
    'start_date': dt.datetime(2022, 2, 2),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


def clean_scooter():
    df = pd.read_csv('/home/javier/scooter.csv')
    df.drop(columns=['region_id'], inplace=True)
    df.columns = [x.lower() for x in df.columns]
    df['started_at'] = pd.to_datetime(df['started_at'], format='%m/%d/%Y %H:%M')
    df.to_csv('/home/javier/cleanscooter.csv')


def filter_data():
    df = pd.read_csv('/home/javier/cleanscooter.csv')
    fromdate = '2019-05-23'
    todate = '2019-06-03'
    filtered_df = df.loc[(df['started_at'] > fromdate) & (df['started_at'] < todate)]
    filtered_df.to_csv('/home/javier/may23-june3.csv')


with DAG(
    'clean_data',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
) as dag:

    clean_data = PythonOperator(
        task_id='clean',
        python_callable=clean_scooter
    )

    select_data = PythonOperator(
        task_id='filter',
        python_callable=filter_data
    )

    copy_file = BashOperator(
        task_id='copy',
        bash_command='cp /home/javier/may23-june3.csv /home/javier/Desktop'
    )

clean_data >> select_data >> copy_file
