# Introduction 
This folder contains the source code and configuration file for installing middle-tier service in ADP boosterpack. The output of the system can be retrieved using the APIs created in this service. This service represents an intermediary layer between the presentation and data service. In this solution, two APIs are created for accessing processed market and news data using FastAPI. While these APIs are supposed to be called by frontend services, they can be accessed using Swagger UI or Redoc interface. For more information, check official FastAPI documentation.  


# Build and Test
The following sections explain how to install and customize this application

## Installing on a Kubernetes cluster 
Run these commands to go to the "middle-tier" folder and instal this service after connecting to the VM using SSH and cloning this repository.
```bash
cd middle-tier
kubectl create namespace middle-tier
kubectl apply -f ./kubernetes-manifests/ -n middle-tier
```

## Deploying changes in the code and build your own image
To make changes in the code, you need to build your own image and push it to your DockerHub or any other container registry. Make sure to update the containers.image parameter in deployement configuration file (middle-tier\kubernetes-manifests\dair-middletier-deployment.yaml). 

```bash
cd middle-tier
docker login
docker build -t {DockerHubAccount}/{ImageName}:{TAG} . 
docker push {DockerHubAccount}/{ImageName}:{TAG} 
```
## Removing the application
To completely remove this application, you need to execute the following commands. If you don't want to delete the namespace, skip running the second command
```bash
kubectl delete deployment dair-middletier -n middle-tier
kubectl delete namespace middle-tier
```

## Accessing APIs Swagger Interface 
This service has been exposed as nodePort on port 30300. The Swagger interface for the APIs of this service can be accessed using this address: *{HOST_IP}:30300/docs*.

