# Introduction 
## Chart repo
https://github.com/bitnami/charts/tree/master/bitnami/kafka

## Helm chart info 
https://artifacthub.io/packages/helm/bitnami/kafka

# Installation
Run these commands to go to the "kafka" folder and installing Apache Kafka using the configured helm chart after connecting to the VM using SSH and cloning this repository.
```bash
cd kafka
helm repo add bitnami https://charts.bitnami.com/bitnami\
helm upgrade -i kafka bitnami/kafka -n data -f values.yaml --debug
```

# Post-deployement Information
    Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:\
        kafka.data.svc.cluster.local

    Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

        kafka-0.kafka-headless.data.svc.cluster.local:9092

    To create a pod that you can use as a Kafka client run the following commands:

        kubectl run kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.1.0-debian-10-r8 --namespace data --command -- sleep infinity
        kubectl exec --tty -i kafka-client --namespace data -- bash

        PRODUCER:
            kafka-console-producer.sh \

                --broker-list kafka-0.kafka-headless.data.svc.cluster.local:9092 \
                --topic test

        CONSUMER:
            kafka-console-consumer.sh \

                --bootstrap-server kafka.data.svc.cluster.local:9092 \
                --topic test \
                --from-beginning
