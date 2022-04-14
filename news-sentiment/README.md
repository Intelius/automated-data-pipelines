# Introduction 
This folder contains the source code and configuration files for installing news sentiment prediction as an example of analytical service in ADP boosterpack. The service uses a pre-trained news sentiment prediction model to predict whether each of the ingested news will have positive, neutral, or negative impact on its related ticker. The sentiment is defined based on the numeric influence scores that are predicted by this NLP-based model. This prediction functionality is exposed as an API using FAST API tool and is being called by news data processing pipeline.   

# Build and Test
The following sections explain how to install and customize this application:

## Installing on a Kubernetes cluster 
Run these commands to go to the "news-sentiment" folder and instal this service after connecting to the VM using SSH and cloning this repository.
```bash
cd news-sentiment
kubectl create namespace news-sentiment
kubectl apply -f ./kubernetes-manifests/ -n news-sentiment
```

## Deploying changes in the code and build your own image
To make changes in the code, you need to build your own image and push it to your DockerHub or any other container registry. Make sure to update the containers.image parameter in deployement configuration file (news-sentiment\kubernetes-manifests\newssentiment-deployment.yaml). 

```bash
cd news-sentiment
docker login
docker build -t {DockerHubAccount}/{ImageName}:{TAG} ./src/newssentiment-service/ 
docker push {DockerHubAccount}/{ImageName}:{TAG} 
```
## Removing the application
To completely remove this application, you need to execute the following commands. If you don't want to delete the namespace, skip running the second command
```bash
kubectl delete deployment newssentiment -n news-sentiment
kubectl delete namespace news-sentiment
```

## Accessing APIs Swagger Interface 
This service has been exposed as nodePort on port 30602. The Swagger interface for the APIs of this service can be accessed using this address: *{HOST_IP}:30602/docs*.