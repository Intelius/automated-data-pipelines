#Installation of the MySQL Operator
#The MYSQL Operator can be installed using kubectl:

#Local files can be used if you need to change any settings

echo "------------------Deploy MySql Operator on Kubernetes--------------------------------------"
echo "============================================================================================"


#Make sure we are correct Kubectl context: 

echo "============================================================================================"

# #IBM Configuration -  Set the login token and the namespace
# export IBMCLOUD_API_KEY=@/home/i2LinDair2021/ibm/keys/key_file
# #Login to IBM Cloud: 
# ibmcloud login -a cloud.ibm.com -r us-south -g i2Trader
# #Set the Kubernetes context to your cluster for this terminal session. 
# ibmcloud ks cluster config --cluster c5vahmod08eltcqga6o0        
# kubectl config current-context
# echo "============================================================================================"

#DAIR Cluster
kubectl config get-contexts
kubectl config use-context microk8s
kubectl config current-context

echo "============================================================================================"

CLUSTER='dev-mysql-cluster'
NAMESPACE='dev-data'

# Helm Install You need to download the sources MySQL Operator for Kubernetes to install the operator with Helm.
# The sources contain a top level directory named helm. 
# export NAMESPACE="mysql-operator"
# helm install mysql-operator helm/mysql-operator --namespace $NAMESPACE --create-namespace

# Or install with kubectl:
kubectl apply -f https://raw.githubusercontent.com/mysql/mysql-operator/trunk/deploy/deploy-crds.yaml
kubectl apply -f https://raw.githubusercontent.com/mysql/mysql-operator/trunk/deploy/deploy-operator.yaml


echo "Note: The propagation of the CRDs can take a few seconds depending on the size of your Kubernetes cluster. Best is to wait a second or two between those
            commands. If the second command fails due to missing CRD apply it a second time. To verify the operator is running check the deployment managing the
            operator, inside the mysql-operator namespace" 

kubectl get deployment -n mysql-operator mysql-operator

# For creating an InnoDB Cluster you first have to create a secret containing credentials for a MySQL root user which is to be created:
kubectl get namespace | grep -q "^$NAMESPACE " || kubectl create namespace $NAMESPACE
kubectl create secret generic dev-mysql-secret \
        --from-literal=rootUser=root \
        --from-literal=rootHost=% \
        --from-literal=rootPassword="QW5hbHl0aWNzMjAyIQ=="  --namespace $NAMESPACE

# cat > dev-mysql-cluster.yaml << EOF
# apiVersion: mysql.oracle.com/v2alpha1
# kind: InnoDBCluster
# metadata:
#   name: dev-mysql-cluster
# spec:
#   secretName: dev-mysql-secret
#   instances: 3
#   router:
#     instances: 1
# EOF

kubectl apply -f ./dev-mysql-cluster.yaml -n $NAMESPACE
echo "============================================================================================"
kubectl get innodbcluster --watch -n $NAMESPACE


#Connecting to the MYSQL InnoDB Cluster -  For connecting to the InnoDB Cluster a Service is created inside the Kubernetes cluster.

kubectl get service $CLUSTER -n $NAMESPACE
kubectl describe service $CLUSTER -n $NAMESPACE


#For a read-write connection to the primary using MYSQL protocol:

#kubectl port-forward service dev-mysql-cluster mysql

