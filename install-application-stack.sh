#!/bin/bash
# Copyright 2022 Intelius Analytics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script needs to run as the root user.

# Please make sure the user matches the one for which you installed and configured Kubernetes


DEFAULTRELEASENAME="helm_chart_upgrade" 
date
echo "Starting Intelius Automated Data Pipelines (ADP) Application Installations"

if [ ! -z $1 ] 
then 
    export RELEASENAME=$1
else
    export RELEASENAME=$DEFAULTRELEASENAME
fi

echo "Installing ADP release $RELEASENAME."

source /etc/environment
export RELEASEDIRNAME="automated-data-pipelines-"$RELEASENAME

if [ ! -z $2 ] 
then 
    export INSTALLUSER=$2
else
    export INSTALLUSER=$(ls /home/* -d | head -n 1 | cut -d/ -f3)
fi
echo -e "\nTargeting user $INSTALLUSER for application-code installation"
export KUBECONFIG=/home/$INSTALLUSER/.kube/config
kubectl config set-context microk8s
cd /home/$INSTALLUSER

echo -e "\n\n Pulling zipped files ..."
rm -rf $RELEASEDIRNAME # Clean out any old run
rm $RELEASENAME.zip
wget https://github.com/Intelius/automated-data-pipelines/archive/$RELEASENAME.zip
unzip $RELEASENAME.zip

echo -e "\n\n Installing K8s Dashboard ..."
cd /home/$INSTALLUSER/$RELEASEDIRNAME/k8sdashboard/
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm repo update
helm upgrade --install k8sdashboard kubernetes-dashboard/kubernetes-dashboard  -f ./dashboard-values.yaml --namespace dashboard --create-namespace

kubectl create namespace data
echo -e "\n\n Installing Apache Kafka ..."
cd /home/$INSTALLUSER/$RELEASEDIRNAME/kafka/
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install kafka bitnami/kafka -n data -f values.yaml

echo -e "\n\n Installing Kafdrop ..."
cd /home/$INSTALLUSER/$RELEASEDIRNAME/kafdrop/
helm upgrade -i kafdrop chart -n data

echo -e "\n\n Installing MySQL preloaded with the solution database schema ..."
cd /home/$INSTALLUSER/$RELEASEDIRNAME/mysql/helm/
kubectl apply -n data -f initdb-config.yaml 
helm repo update
helm install my-release bitnami/mysql -n data -f values.yaml

echo -e "\n\n Installing News Sentiment Prediction service ..."
cd /home/$INSTALLUSER/$RELEASEDIRNAME/news-sentiment
kubectl create namespace news-sentiment
kubectl apply -f ./kubernetes-manifests/ -n news-sentiment

echo -e "\n\n Installing Apache Airflow ..."
cd /home/$INSTALLUSER/$RELEASEDIRNAME/airflow/
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm install airflow ./chart/ -f ./values.yaml -n airflow --create-namespace
kubectl exec airflow-worker-0 -n airflow -- airflow variables set POLYGON_API_KEY $POLYGON_API_KEY
kubectl exec airflow-worker-0 -n airflow -- airflow variables set FINNHUB_API_KEY $FINNHUB_API_KEY

echo -e "\n\n Installing Middle-Tier Services ..."
cd /home/$INSTALLUSER/$RELEASEDIRNAME/middle-tier
kubectl create namespace middle-tier
kubectl apply -f ./kubernetes-manifests/ -n middle-tier

echo -e "\n\n Installing Fontend (Presentation) Services ..."
cd /home/$INSTALLUSER/$RELEASEDIRNAME/frontend
kubectl create namespace frontend
host_ip="$(dig +short myip.opendns.com @resolver1.opendns.com)"
kubectl create secret generic host-name --from-literal=API_URL_ROOT=http://${host_ip}:30300 -n frontend
kubectl apply -f ./kubernetes-manifests/ -n frontend

echo -e "\n\n Finalizing the installation ..."
chown -R $INSTALLUSER:$INSTALLUSER /home/$INSTALLUSER/$RELEASEDIRNAME/
cd /home/$INSTALLUSER
rm $RELEASENAME.zip

printf "\n\nCongratulations! Intelius Automated Data Pipelines (ADP) boosterpack has been successfully installed!"
