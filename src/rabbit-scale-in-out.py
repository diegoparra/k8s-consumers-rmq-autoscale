import pika
import os
from kubernetes import client, config

def queueCheck(rabbit_username, rabbit_password, rabbit_url, rabbit_port, rabbit_queue):
    credentials = pika.PlainCredentials(rabbit_username, rabbit_password)
    parameters = pika.ConnectionParameters(rabbit_url,
                                        rabbit_port,
                                        '/',
                                        credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # Declare the queue
    channel.queue_declare(
        queue=rabbit_queue,
        durable=True,
        exclusive=False,
        auto_delete=False
    )

    res = channel.queue_declare(
        queue=rabbit_queue,
        durable=True,
        exclusive=False,
        auto_delete=False,
        passive=True
    )
    #print('Messages in queue %d' % res.method.message_count)
    return res.method.message_count

def deploymentScale(name, replicas, namespace):
    config.load_kube_config()
    k8s_apps_v1 = client.AppsV1Api()
    body = {'spec': {'replicas': replicas}}
    resp = k8s_apps_v1.patch_namespaced_deployment(
        body=body, namespace=namespace, name=name)
    print("Deployment updated. status='%s'" % str(resp.status))

def getPods(name):
    config.load_kube_config()
    k8s_apps_v1 = client.CoreV1Api()
    # k8s_apps_v1 = client.AppsV1Api()
    resp = k8s_apps_v1.list_pod_for_all_namespaces(
        label_selector=name, pretty="pretty", watch=False)
    return resp
    

def main():

    # Setup variables
    rabbit_username = os.environ['RABBIT_USER']
    rabbit_password = os.environ['RABBIT_PASSWORD']
    rabbit_url = os.environ['RABBIT_URL']
    rabbit_port = os.environ['RABBIT_PORT']
    rabbit_queue = os.environ['RABBIT_QUEUE']  
    pod_name = os.environ['POD_NAME']
    app_name = os.environ['DEPLOYMENT_NAME']
    app_namespace = os.environ['APP_NAMESPACE']
    first_scale = os.environ['FIRST_SCALE']
    second_scale = os.environ['SECOND_SCALE']
    third_scale = os.environ['THIRD_SCALE']


    pods = getPods(pod_name)
    pods_total = 0
    for pod in pods.items:
        print("Podname: {}".format(pod))
        pods_total += 1
        size = queueCheck(rabbit_username, rabbit_password, rabbit_url, rabbit_port, rabbit_queue)
        if size >= first_scale and pods_total <= 2:
            print("Queue has more then 5M, scaling to 3 Containers")
            deploymentScale(app_name, 3, app_namespace)
        elif size >= second_scale and pods_total <= 3:
            print("Queue has more then 10M, scaling to 4 Containers")
            deploymentScale(app_name, 4, app_namespace)
        elif size >= third_scale and pods_total <= 4:
            print("Queue has more then 15M, scaling to 5 Containers")
            deploymentScale(app_name, 5, app_namespace)
        else:
            print("Scale up not necessary, checking scale down...")
            if size < first_scale and pods_total >= 2:
                print("Queue has less then 5M, scaling down to 1 Container")
                deploymentScale(app_name, 1, app_namespace)
                print("Queue size ok")

if __name__ == '__main__':
    main()