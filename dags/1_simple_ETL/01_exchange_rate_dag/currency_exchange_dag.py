from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import datetime
import os
import requests
import json 
from io import StringIO 


S3_BUCKET = os.getenv('S3_BUCKET')
api_key = os.getenv('api_key')
print(api_key)



def get_data_from_API_and_savein_S3(): 
    date = datetime.today().strftime("%Y%m%d")
    # get the most recent exchange rate data
    # i change to another free api, no api_key needed

    
    url = f"https://api.exchangerate.host/latest"
    headers = {
          "Accept": "application/json",
          "Connection": "keep-alive",
            }
    response = requests.get(url = url, headers=headers)
    json_file = response.json()

    # remove unrelated columns
    del json_file['motd']
    del json_file['success']

    string =  json.dumps(json_file)
    fp = StringIO(string)
    s3_hook = S3Hook(aws_conn_id = 's3_connection', region_name = 'us-east-2')
    s3_hook.load_string(fp.getvalue(), f'currency_exchange_rate/exchange_rate_{date}.json', bucket_name = S3_BUCKET, replace = True)
    print(fp.getvalue())
    return "SUCCESSFULLY"



my_dag = DAG(
    dag_id='currency_exchange_etl',
    start_date=datetime(2023, 6, 11),
    schedule_interval='@daily'
)

start = DummyOperator(
    task_id='start',
    dag=my_dag
)

get_data = PythonOperator(task_id='extract_data_via_api_and_load_on_S3', 
                          python_callable = get_data_from_API_and_savein_S3,
                          op_kwargs = {
                              'api_key': api_key
                          },
                          dag=my_dag)
end = DummyOperator(
    task_id='end',
    dag=my_dag
)
start >> get_data >> end
