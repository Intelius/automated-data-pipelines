# Installation
## Build Docker container
docker login
cd airflow
docker build -t inteliusai/dair_boosterpack_airflow:1.0 . 
docker push inteliusai/dair_boosterpack_airflow:1.0 

# update git repo on the server after SSH
cd app/airflow
git pull

 [optional] kubectl create namespace airflow
 [optional] helm repo add apache-airflow https://airflow.apache.org/
helm delete airflow -n airflow
helm upgrade --install airflow apache-airflow/airflow --namespace airflow -f values.yaml --debug
