import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch, helpers


def query_postgresql():
    conn_string = "dbname='dataengineering' " \
                  "host='localhost' " \
                  "user='postgres' " \
                  "password='postgres'"
    conn = db.connect(conn_string)
    df = pd.read_sql('select name, city from users', conn)
    df.to_csv('../../../postgresqldata.csv')
    print('------DATA SAVED------')


# This can be done with actions and helpers.bulk()
def insert_elasticsearch():
    es = Elasticsearch()
    df = pd.read_csv('../../../postgresqldata.csv')

    actions = []
    for i, row in df.iterrows():
        action = {
                '_op_type': 'index',
                '_index': 'users2',
                '_source': {
                    'name': row['name'],
                    'city': row['city']
                }}
        actions.append(action)
        while i > 1000:
            break

    response = helpers.bulk(client=es, actions=actions, index='users2')
    print("\nRESPONSE:", response)


default_args = {
    'owner': 'javier',
    'start_date': dt.datetime(2022, 2, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG(
    'MyDBdag',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5), # '0 * * * *',
) as dag:

    get_data = PythonOperator(
        task_id='QueryPostgreSQL',
        python_callable=query_postgresql
    )

    insert_data = PythonOperator(
        task_id='InserDataElasticsearch',
        python_callable=insert_elasticsearch
    )

get_data >> insert_data
