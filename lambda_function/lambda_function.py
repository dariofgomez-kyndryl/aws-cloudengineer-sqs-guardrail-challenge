# SecretCode: dariofgomez-kyndryl-2025-XYZ
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs_client = boto3.client('sqs')
kms_client = boto3.client('kms')
ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    for record in event.get("Records", []):
        if record.get("eventSource") == "aws:sqs":
            queue_url = record.get("eventSourceARN")
            
            if not queue_url:
                logger.error("Queue URL not found in event.")
                continue
            
            queue_attributes = sqs_client.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=["All"]
            )
            
            if not check_vpc_endpoint():
                send_alert(f"No VPC endpoint found for SQS.")
            if not check_encryption(queue_attributes):
                send_alert(f"Queue {queue_url} is not encrypted with a CMK.")
            if not check_tags(queue_url):
                send_alert(f"Queue {queue_url} is missing required tags.")
    
    return {
        'statusCode': 200,
        'body': json.dumps('SQS Guardrail Check Completed.')
    }

#function to validate VPC endpoint exists
def check_vpc_endpoint():
    vpc_endpoints = ec2_client.describe_vpc_endpoints(
        Filters=[{"Name": "service-name", "Values": ["com.amazonaws.us-east-1.sqs"]}]
    )
    return len(vpc_endpoints.get("VpcEndpoints", [])) > 0

#function to validate CMK encryption
def check_encryption(attributes):
    return attributes.get("Attributes", {}).get("KmsMasterKeyId") is not None

#function to validate required Tags
def check_tags(queue_url):
    required_tags = {"Name", "Created By", "Cost Center"}
    tags = sqs_client.list_queue_tags(QueueUrl=queue_url).get("Tags", {})
    return required_tags.issubset(tags.keys())

def send_alert(message):
    logger.error(message)
    if sns_client:
        sns_client.publish(
            TopicArn="sns-topic-arn",
            Message=message
        )