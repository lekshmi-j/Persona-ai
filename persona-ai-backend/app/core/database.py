import boto3
from app.core.config import settings

def get_dynamodb_resource():
    """
    Returns a boto3 DynamoDB resource.
    Uses DYNAMODB_ENDPOINT from .env for local dev.
    In production (real AWS), remove the endpoint_url
    and it will connect to AWS automatically.
    """
    return boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.DYNAMODB_ENDPOINT,
    )

def get_dynamodb_client():
    """
    Returns a boto3 DynamoDB client.
    Use this for operations like creating tables.
    Use get_dynamodb_resource() for put/get/delete items.
    """
    return boto3.client(
        "dynamodb",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.DYNAMODB_ENDPOINT,
    )

# Single shared instances — import these directly in other files
dynamodb = get_dynamodb_resource()
dynamodb_client = get_dynamodb_client()