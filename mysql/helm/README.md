# Introduction 
Installation of MySQL on a Kubernetes cluster using bitnami helm chart
## Chart repo
https://github.com/bitnami/charts/tree/master/bitnami/mysql

## Helm chart info 
https://artifacthub.io/packages/helm/bitnami/mysql

# Deployed Information
Services:

  echo Primary: my-release-mysql.data.svc.cluster.local:3306

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