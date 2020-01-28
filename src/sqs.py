import boto3

client = boto3.client('sqs')

response = client.get_queue_attributes(
            QueueUrl="my-sqs-queue-endpoint",
            AttributeNames=['ApproximateNumberOfMessages']
        )
        
print(int(response['Attributes']['ApproximateNumberOfMessages']))