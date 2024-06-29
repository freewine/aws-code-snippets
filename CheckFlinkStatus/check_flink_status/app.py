# import requests

import boto3
import json
import os
import datetime
from botocore.exceptions import ClientError

# 创建 STS和Sagemaker 客户端
flink_client = boto3.client("kinesisanalyticsv2")
dynamodb_client = boto3.client("dynamodb")
sns_client = boto3.client('sns')

# Specify the table name
table_name = 'ManagedFlinkAppStatus'

# 读取环境变量
sns_topic_arn = os.environ.get('SNS_TOPICS_ARN')

def lambda_handler(event, context):
    print(event)

    action = event.get('action')

    if action == "check status":
        checkStatusChange()

    return {
        'statusCode': 200,
        'body': json.dumps({'result': 'Success'})
    }

def sendSNS(message):
    try:
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='Flink Application Status Change'
        )
        print(f"SNS response: {response}")
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")

def checkStatusChange():
    app_list = flink_client.list_applications()['ApplicationSummaries']
    print(f'app_list: {app_list}')
    for app in app_list:
        try:
            app_item = dynamodb_client.get_item(
                TableName=table_name,
                Key={
                    'ApplicationName': {'S': app['ApplicationName']}
                }
            )

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if 'Item' in app_item:
                print(f"Retrieved item: {app_item['Item']}")
                if(app_item['Item']['ApplicationStatus']['S'] != app['ApplicationStatus']):
                    message = f"The application {app['ApplicationName']} status has changed from {app_item['Item']['ApplicationStatus']['S']} to {app['ApplicationStatus']}."
                    sendSNS(message)
                    dynamodb_client.update_item(
                        TableName=table_name,
                        Key={
                            'ApplicationName': {'S': app['ApplicationName']}
                        },
                        UpdateExpression="SET ApplicationStatus = :s, UpdatedAt = :t",
                        ExpressionAttributeValues={
                            ':s': {'S': app['ApplicationStatus']},
                            ':t': {'S': f'{now}'}
                        }
                    )
                else:
                    dynamodb_client.update_item(
                        TableName=table_name,
                        Key={
                            'ApplicationName': {'S': app['ApplicationName']}
                        },
                        UpdateExpression="SET UpdatedAt = :t",
                        ExpressionAttributeValues={
                            ':t': {'S': f'{now}'}
                        }
                    )
            else:
                print("The item was not found.")
                new_item = {
                    'ApplicationName': {'S': app['ApplicationName']},
                    'ApplicationStatus': {'S': app['ApplicationStatus']},
                    'ApplicationVersionId': {'N': str(app['ApplicationVersionId'])},
                    'RuntimeEnvironment': {'S': app['RuntimeEnvironment']},
                    'ApplicationMode': {'S': app['ApplicationMode']},
                    'UpdatedAt': {'S': f'{now}'},
                }
                dynamodb_client.put_item(
                    TableName=table_name,
                    Item=new_item
                )
                message = f"A new application {app['ApplicationName']} has been added with status {app['ApplicationStatus']}."
                sendSNS(message)
        except ClientError as e:
            print(f"Error: {e.response['Error']['Message']}")
