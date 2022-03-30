import sys
sys.path.append("./dags/")
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import DAG
from datetime import datetime
from src.newsdataprocessing import DailyNewsPolygonMain
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
    'start_date': days_ago(1),
    'catchup': False,
    'provide_context': True,
    'on_failure_callback': task_failure_callback,
}

with DAG(
    'news-processing',
    description='Live News Processing DAG',
    schedule_interval='*/5 * * * *',
    default_args=default_args
) as dag: 

    process_live_news_from_polygonio = PythonOperator(
        task_id='process_news',
        provide_context=True,
        python_callable= DailyNewsPolygonMain,
        dag=dag,
    )

    process_live_news_from_polygonio
