import boto3
import sys
import os

# Add the parent folder to Python path so we can import from app/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

def get_client():
    return boto3.client(
        "dynamodb",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.DYNAMODB_ENDPOINT,
    )

def create_personas_table(client):
    """Creates the Personas table if it doesn't already exist."""
    try:
        client.create_table(
            TableName="Personas",
            KeySchema=[
                {"AttributeName": "persona_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "persona_id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print("✓ Personas table created")
    except client.exceptions.ResourceInUseException:
        print("→ Personas table already exists, skipping")

def create_users_table(client):
    """Creates the Users table if it doesn't already exist."""
    try:
        client.create_table(
            TableName="Users",
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print("✓ Users table created")
    except client.exceptions.ResourceInUseException:
        print("→ Users table already exists, skipping")

if __name__ == "__main__":
    print("Creating DynamoDB tables...")
    client = get_client()
    create_personas_table(client)
    create_users_table(client)
    print("Done!")