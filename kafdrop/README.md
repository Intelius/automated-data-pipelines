# Introduction 
Installation of Kafdrop as the web UI for Kafka
## Chart repo
https://github.com/obsidiandynamics/kafdrop

## Helm chart info 
https://artifacthub.io/packages/helm/main/kafdrop

# Installation 
Run these commands to go to the "kafdrop" folder and instal Kafdrop using the configured helm chart after connecting to the VM using SSH and cloning this repository. 
```bash
cd kafdrop
helm upgrade -i kafdrop chart -n data
```
# Accessing Kafdrop
This service has been exposed as nodePort on port 30900. The UI for this service can be accessed using this address: *{HOST_IP}:30900*.