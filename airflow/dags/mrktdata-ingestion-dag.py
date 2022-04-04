from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import ShortCircuitOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.dates import days_ago
from airflow.models import DAG
from datetime import datetime
import src.mrktdataingestion as mdi
import dagutils

# Enter your email to receive task failure emails 
ALERT_EMAIL_ADDRESSES = "support-email@test.com"

def checkWeekdayHrs(**context):
    try:
        next_execution_date = context['next_execution_date']   
        isweekday = dagutils.checkweekday(next_execution_date,'M-F')
        return (isweekday and dagutils.checkmarkethrs())
    except:
        return False

def task_failure_callback(context):
	outer_task_callback(context, email=ALERT_EMAIL_ADDRESSES, result="Failed")

def outer_task_callback(context, email, result):
    try:
        subject = "[Airflow] DAG {0} - Task {1}: {2}".\
            format(context['task_instance_key_str'].split('__')[0],\
                context['task_instance_key_str'].split('__')[1], result)
        html_content = "DAG: {0}<br>Task: {1}<br>{3} on: {2}".\
            format(context['task_instance_key_str'].split('__')[0],\
                context['task_instance_key_str'].split('__')[1],datetime.now(),result)

        dagutils.sendemails(email, subject, html_content)
    except Exception as e:
        print(e.message) 

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'provide_context': True,
    'email': ALERT_EMAIL_ADDRESSES,
    'email_on_failure' : True,
    'email_on_retry': False,
    'on_failure_callback': task_failure_callback,
}

with DAG(
    'marketdata-inestion-1min',
    description='Live 1-min aggregated market mata ingestion dag',
    schedule_interval='0-59/1 13-21 * * 1-5',
    catchup=False,
    default_args=default_args
) as dag:

    start_dummy = DummyOperator(
        task_id='start',
        dag=dag
    )

    end_dummy = DummyOperator(
        task_id='end',
        trigger_rule=TriggerRule.NONE_FAILED,
        dag=dag
    )

    check_weekdays_hrs = ShortCircuitOperator(
        task_id='check_weekdays_hrs',
        python_callable=checkWeekdayHrs,
        dag=dag
    )

    ingest_live_data_to_bronze = PythonOperator(
        task_id='ingest_live_market_data',
        provide_context=True,
        python_callable=mdi.marketdataingestion,
        dag=dag,
    )

    start_dummy >> check_weekdays_hrs >> ingest_live_data_to_bronze >> end_dummy
