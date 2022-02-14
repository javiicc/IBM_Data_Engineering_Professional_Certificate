from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import datetime as dt
from datetime import timedelta
import pandas as pd


default_args = {
    'owner': 'javier',
    'start_date': dt.datetime(2022, 2, 10),
    'email': 'javiercastanocandela@hotmail.com',
    'emailonfailure': True,
    'emailonretry': True,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

dag = DAG(
    dag_id='ETL_toll_data',
    schedule_interval='@daily',
    default_args=default_args,
    description='Apache Airflow Final Assignment'
)


unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command=(
        'tar zxvf /home/javier/airflow/dags/finalassignment/tolldata.tgz '
        '-C /home/javier/airflow/dags/finalassignment'
    ),
    dag=dag
)


def extract_and_save_columns_csv():
    df = pd.read_csv('/home/javier/airflow/dags/finalassignment/vehicle-data.csv', header=None)
    df = df.iloc[:, 0:4]
    df.to_csv('/home/javier/airflow/dags/finalassignment/csv_data.csv', index=False)


extract_data_from_csv = PythonOperator(
    task_id='extract_data_from_csv',
    python_callable=extract_and_save_columns_csv,
    dag=dag
)


def extract_and_save_columns_tsv():
    df = pd.read_csv('/home/javier/airflow/dags/finalassignment/tollplaza-data.tsv', sep='\t', header=None)
    df = df.iloc[:, 4:7]
    df.to_csv('/home/javier/airflow/dags/finalassignment/tsv_data.csv', index=False, sep=',')


extract_data_from_tsv = PythonOperator(
    task_id='extract_data_from_tsv',
    python_callable=extract_and_save_columns_tsv,
    dag=dag
)


def extract_and_save_columns_fwf():
    df = pd.read_fwf('/home/javier/airflow/dags/finalassignment/payment-data.txt', colspecs='infer', header=None)
    df = df.iloc[:, -2:]
    df.to_csv('/home/javier/airflow/dags/finalassignment/fixed_width_data.csv', index=False, sep=',')


extract_data_from_fixed_width = PythonOperator(
    task_id='extract_data_from_fwf',
    python_callable=extract_and_save_columns_fwf,
    dag=dag
)


def consolidate_3_to_1():
    csv_data = pd.read_csv('/home/javier/airflow/dags/finalassignment/csv_data.csv').reset_index(drop=True)
    tsv_data = pd.read_csv('/home/javier/airflow/dags/finalassignment/tsv_data.csv').reset_index(drop=True)
    fixed_width_data = pd.read_csv('/home/javier/airflow/dags/finalassignment/fixed_width_data.csv'
                                   ).reset_index(drop=True)

    df = csv_data.merge(tsv_data, left_index=True, right_index=True)\
                 .merge(fixed_width_data, left_index=True, right_index=True)

    df.to_csv('/home/javier/airflow/dags/finalassignment/transformed_data.csv')


consolidate_data = PythonOperator(
    task_id='consolidate_data',
    python_callable=consolidate_3_to_1,
    dag=dag
)


def transform_data():
    df = pd.read_csv('/home/javier/airflow/dags/finalassignment/extracted_data.csv', header=None)[1:]

    # Something was wrong here so I solved it by implementing the code bellow
    df.iloc[:, 4] = df.iloc[:, 4].str.split("\t").str[0]
    df.iloc[:, 7] = df.iloc[:, 7].str.split("\t").str[0]

    df.iloc[:, 4] = df.iloc[:, 4].str.upper()
    df.to_csv('/home/javier/airflow/dags/finalassignment/transformed_data.csv')
    print('-'*30)
    print(df.sample(3))
    print(df.iloc[:, 4])
    print(df.iloc[:, 7])


transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)


unzip_data >> [extract_data_from_csv, extract_data_from_tsv, extract_data_from_fixed_width] >> consolidate_data
consolidate_data >> transform_data
