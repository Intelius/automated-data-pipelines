# Introduction 
    The Kafka Helm Chart deployment
    Original git hub: https://github.com/bitnami/charts/tree/master/bitnami/kafka
    Release number: 15.3.2

# Getting Started
    This repository contains the configurations for kafka cluster for deployment on any Kubernetes cluser clusters
    1.	By cloning this repo and running "helm install <<release_name>> bitnami/kafka -f values.yaml" the chart will be installed using the configurations existing in the values.yaml file.
    2.	This can only be tested on a k8s cluster and can't be deployed standalone.

# Installation
    Run the following command:
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm upgrade -i kafka bitnami/kafka -n data -f values.yaml --debug

# Deployed Information
    Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

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
