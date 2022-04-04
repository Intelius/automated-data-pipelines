from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import DAG
from datetime import datetime
import src.mrktdataprocessing as mdp
import dagutils

# Enter your email to receive task failure emails 
ALERT_EMAIL_ADDRESSES = "support-email@test.com"

def task_failure_callback(context):
	outer_task_callback(context, email=ALERT_EMAIL_ADDRESSES, result="Failed")

def outer_task_callback(context, email, result):
    subject = "[Airflow] DAG {0} - Task {1}: {2}".\
        format(context['task_instance_key_str'].split('__')[0],\
            context['task_instance_key_str'].split('__')[1], result)
    html_content = "DAG: {0}<br>Task: {1}<br>{3} on: {2}".\
        format(context['task_instance_key_str'].split('__')[0],\
            context['task_instance_key_str'].split('__')[1],datetime.now(),result)      
    try:
        dagutils.sendemails(email, subject, html_content)
    except Exception as e:
        print(e.message) 

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'concurrency': 1, 
    'start_date': days_ago(1),
    'provide_context': True,
    'on_failure_callback': task_failure_callback
}

with DAG(
    'marketdata-processing-1min',
    description='Live 1-min aggregated market data processing dag',
    schedule_interval='30 13 * * 1-5',
    catchup=False,
    default_args=default_args
    ) as dag:

    process_live_data = PythonOperator(
        task_id='process_1min_live_market_data',
        provide_context=True,
        python_callable=mdp.marketdataprocessing,
        dag=dag,
    )
    
    process_live_data
    