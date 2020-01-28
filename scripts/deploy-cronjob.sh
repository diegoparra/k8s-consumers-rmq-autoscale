
# Defining your variables
export APP_NAME="MyAPP"
export SCHEDULE="*/10 * * * *" #every 10 minutes
export DOCKER_IMAGE="your-docker-image"
export CLUSTER_NAME="your-cluster-name"
export AWS_REGION="aws-region"
export APP_NAMESPACE="app-namespace"
export DEPLOYMENT_NAME="deployment-name"
export POD_NAME="app=pod-name"
export FIRST_SCALE="5000000" #5m messages
export SECOND_SCALE="10000000" #10m messages
export THIRD_SCALE="15000000" #15m messages
export RABBIT_URL="your-rabbit-url"
export RABBIT_QUEUE="your-rabbit-queue"


cat manifests/cronjob.yml | \
sed "s|{{ APP_NAME }}|${APP_NAME}|g" | \
sed "s|{{ SCHEDULE }}|${SCHEDULE}|g" | 
sed "s|{{ DOCKER_IMAGE }}|${DOCKER_IMAGE}|g" | \
sed "s|{{ CLUSTER_NAME }}|${CLUSTER_NAME}|g" | \
sed "s|{{ AWS_REGION }}|${AWS_REGION}|g" | \
sed "s|{{ APP_NAMESPACE }}|${APP_NAMESPACE}|g" | \
sed "s|{{ DEPLOYMENT_NAME }}|${DEPLOYMENT_NAME}|g" | \
sed "s|{{ POD_NAME }}|${POD_NAME}|g" | \
sed "s|{{ FIRST_SCALE }}|${FIRST_SCALE}|g" | \
sed "s|{{ SECOND_SCALE }}|${SECOND_SCALE}|g" | \
sed "s|{{ THIRD_SCALE }}|${THIRD_SCALE}|g" | \
sed "s|{{ RABBIT_URL }}|${RABBIT_URL}|g" | \
sed "s|{{ RABBIT_QUEUE }}|${RABBIT_QUEUE}|g" | \
kubectl apply -f -




