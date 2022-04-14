# Introduction 
Installation of MySQL on a Kubernetes cluster using bitnami helm chart
## Chart repo
https://github.com/bitnami/charts/tree/master/bitnami/mysql

## Helm chart info 
https://artifacthub.io/packages/helm/bitnami/mysql

# Installation 
Run these commands to go to the "mysql/helm/" folder and installing MySQL using the configured helm chart after connecting to the VM using SSH and cloning this repository. MySQL will be preloaded with the schema defined in the initdb-config.yaml file. Update DDL commands in this file based on your need before installation.
```bash
cd mysql/helm/
kubectl apply -n data -f initdb-config.yaml 
helm install my-release bitnami/mysql -n data -f values.yaml
```
Default credentials for creating a connection to this MySQL instance:\
&nbsp;&nbsp;&nbsp;&nbsp;user: root\
&nbsp;&nbsp;&nbsp;&nbsp;pass: BoosterPack202!
# Post-deployement Information
  Execute the following to get the administrator credentials:

    echo Username: root
    MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace data my-release-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)

  To connect to your database:

    1. Run a pod that you can use as a client:

        kubectl run my-release-mysql-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mysql:8.0.27-debian-10-r8 --namespace data --command -- bash

    2. To connect to primary service (read/write):

        mysql -h my-release-mysql.data.svc.cluster.local -uroot -p"$MYSQL_ROOT_PASSWORD"

  To upgrade this helm chart:

    1. Obtain the password as described on the 'Administrator credentials' section and set the 'root.password' parameter as shown below:

        ROOT_PASSWORD=$(kubectl get secret --namespace data my-release-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)
        helm upgrade --namespace data my-release bitnami/mysql --set auth.rootPassword=$ROOT_PASSWORD