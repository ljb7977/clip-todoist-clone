import json
import boto3

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('users')

user = {
    'id': 'etranger',
    'name': 'suho',
}

def create(event, context):
    print(event)
    
    user_table.put_item(
        Item = user
    )
    body = {
        "message": "User Create Function",
        "input": event,
        "user": user
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(user)
    }

    return response

def get(event, context):
    user = user_table.get_item(
        Key={ 'id': 'etranger'}
    )
    response = {
        "statusCode": 200,
        "body": json.dumps(user)
    }
    print(event)
    print(response)
    return response


def handler (event, context):
    print(event)
    print(event.httpMethod)
    print(context)

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
