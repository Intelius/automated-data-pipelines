# Introduction 
This folder contains the configuration file for installing Apache Airflow using its official helm chart and the source code of data pipelines in the ADP boosterpack.

## Chart repo
https://github.com/apache/airflow

## Helm chart info 
https://artifacthub.io/packages/helm/apache-airflow/airflow 

# Build and Test
The following sections explain how to install and customize this application

## Installing on a Kubernetes cluster 
Run these commands to go to the "airflow" folder and installing Airflow using the configured helm chart after connecting to the VM using SSH and cloning this repository.
```bash
cd airflow
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f values.yaml --debug
```

## Deploying changes in the code and build your own image
To make changes in the code, you need to build your own image and push it to your DockerHub or any other container registry. Make sure to update *images.flower.repository* and *images.flower.tag* in your airflow helm values file (airflow/values.yaml). Alternative, you can add these arguments to the above "helm upgrade" command: *--set images.flower.repository={DockerHubAccount}/{ImageName} -- set images.flower.tag={TAG}*

```bash
cd airflow
docker login
docker build -t {DockerHubAccount}/{ImageName}:{TAG} . 
docker push {DockerHubAccount}/{ImageName}:{TAG} 
```
## Removing the application
To completely remove this application, you need to execute the following commands. If you don't want to delete the namespace, skip running the second command
```bash
helm delete airflow -n airflow
kubectl delete namespace airflow
```

## Accessing Airflow UI
Airflow webserver service has been exposed as nodePort. The Airflow UI can be accessed using this address: {HOST_IP}:{NODEPORT}. The nodePort number can be found in the detailed information of this service on Kubernetes Dashboard. Alternatively, if you have connected to the VM using SSH or console, you can get this number after running this command:
```bash
kubectl describe service airflow-webserver -n airflow
```

Default Webserver (Airflow UI) Login credentials: \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;username: admin\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;password: admin\
\
You can chage this password in the Helm chart values file before the installation or in the UI after logging in.

