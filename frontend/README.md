# Introduction 
This folder contains the source code and configuration file for installing frontend service in ADP boosterpack. This service provides an interface that enables users to access the outputs of the system. In this solution, a web page gets deployed that presents a ticker market data using a candlestick chart and recent news information, including their sentiment, after selecting a ticker and a date. This web page is developed using React.js technology.

# Build and Test
The following sections explain how to install and customize this application

## Installing on a Kubernetes cluster 
Run these commands to go to the "frontend" folder and instal this service after connecting to the VM using SSH and cloning this repository.
```bash
cd frontend
kubectl create namespace frontend
kubectl apply -f ./kubernetes-manifests/ -n frontend
```

## Deploying changes in the code and build your own image
To make changes in the code, you need to build your own image and push it to your DockerHub or any other container registry. Make sure to update the containers.image parameter in deployement configuration file (frontend\kubernetes-manifests\dair-app-deployment.yaml). 

```bash
cd frontend
docker login
docker build -t {DockerHubAccount}/{ImageName}:{TAG} . 
docker push {DockerHubAccount}/{ImageName}:{TAG} 
```
## Removing the application
To completely remove this application, you need to execute the following commands. If you don't want to delete the namespace, skip running the second command
```bash
kubectl delete deployment dair-app -n frontend
kubectl delete namespace frontend
```

## Accessing UI
This service has been exposed as nodePort on port 30333. The UI for this service can be accessed using this address: *{HOST_IP}:30333*.

