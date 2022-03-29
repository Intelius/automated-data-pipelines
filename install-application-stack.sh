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

# There are two command line arguments (both optional) but quite important to understand
# $1 is the RELEASENAME you want to install from github
# $2 is the USER for whom to install this.

# Please make sure the user matches the one for which you installed and configured Kubernetes


DEFAULTRELEASENAME="main" 
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
export RELEASEDIRNAME="automated-data-pipelines-toolkit-"$RELEASENAME

if [ ! -z $2 ] 
then 
    export INSTALLUSER=$2
else
    export INSTALLUSER=$(ls /home/* -d | head -n 1 | cut -d/ -f3)
fi
echo "Targeting user $INSTALLUSER for application-code installation"
export KUBECONFIG=/home/$INSTALLUSER/.kube/config
kubectl config set-context microk8s
cd /home/$INSTALLUSER

# Pull zipped files
rm -rf $RELEASEDIRNAME # Clean out any old run
rm $RELEASENAME.zip
wget https://github.com/Intelius/automated-data-pipelines/$RELEASENAME.zip
unzip $RELEASENAME.zip

# K8s Dashboard
cd /home/$INSTALLUSER/$RELEASEDIRNAME/code/k8sdashboard/
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm repo update
helm upgrade --install k8sdashboard kubernetes-dashboard/kubernetes-dashboard  -f ./dashboard-values.yaml --namespace dashboard --create-namespace

# Airflow
cd /home/$INSTALLUSER/$RELEASEDIRNAME/code/airflow/
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm install airflow apache-airflow/airflow -n airflow --create-namespace -f values.yaml

# Kafka
cd /home/$INSTALLUSER/$RELEASEDIRNAME/code/kafka/
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install kafka bitnami/kafka -n data --create-namespace -f values.yaml

#Kafdrop
cd /home/$INSTALLUSER/$RELEASEDIRNAME/code/kafdrop/
helm upgrade -i kafdrop chart -n data

# MySQL
cd /home/$INSTALLUSER/$RELEASEDIRNAME/code/mysql/helm/
# kubectl create configmap mysql-initdb-config --from-file=initScript.properties -n test-mysql
helm install my-release bitnami/mysql -n data -f values.yaml

# News Sentiment
cd /home/$INSTALLUSER/$RELEASEDIRNAME/code/news-sentiment
kubectl create namespace news-sentiment
kubectl apply -f ./kubernetes-manifests/ -n news-sentiment

# Middle-Tier
cd /home/$INSTALLUSER/$RELEASEDIRNAME/code/middle-tier
kubectl create namespace middle-tier
kubectl apply -f ./kubernetes-manifests/ -n middle-tier

# Fontend
cd /home/$INSTALLUSER/$RELEASEDIRNAME/code/frontend
kubectl create namespace frontend
host_ip="$(dig +short myip.opendns.com @resolver1.opendns.com)"
kubectl create secret generic host-name --from-literal=API_URL_ROOT=http://${host_ip}:30300 -n frontend
kubectl apply -f ./kubernetes-manifests/ -n frontend

chown -R $INSTALLUSER:$INSTALLUSER /home/$INSTALLUSER/$RELEASEDIRNAME/
cd /home/$INSTALLUSER
rm $RELEASENAME.zip

echo "Congratulations! Intelius Automated Data Pipelines (ADP) boosterpack has been successfully installed!"
