FROM apache/airflow:2.2.1-python3.7

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

USER root

COPY --chown=airflow:root ./dags/ ${AIRFLOW_HOME}/dags/
RUN mkdir -p /opt/airflow/logs 
RUN mkdir -p /opt/airflow/plugins

USER airflow
