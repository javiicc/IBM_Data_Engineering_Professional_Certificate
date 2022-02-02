import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd


def csv_to_json():
    df = pd.read_csv('/home/javier/Desktop/IBM_Data_Engineering/IBM_git/'
                     'Data_Engineering_with_Python_Book/data.csv')

    for i, r in df.iterrows():
        print(r['name'])

    df.to_json('/home/javier/Desktop/IBM_Data_Engineering/'
               'fromairflow.json', orient='records')


default_args = {
    'owner': 'javier',
    'start_date': dt.datetime(2022, 1, 24),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('MycsvDAG',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5)
         ) as dag:

    print_starting = BashOperator(task_id='starting',
                                  bash_command='echo "I am reading '
                                               'the csv now..."')

    csv_json = PythonOperator(task_id='convert-csv-to-json',
                              python_callable=csv_to_json)

print_starting >> csv_json
