from boto3.dynamodb.conditions import Key
from app.core.database import dynamodb
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)

def get_table(table_name: str):
    """Returns a DynamoDB table resource by name."""
    return dynamodb.Table(table_name)

def put_item(table_name: str, item: dict) -> bool:
    """
    Saves an item to DynamoDB.
    Overwrites existing item if the partition key matches.
    Returns True on success, False on failure.
    """
    try:
        table = get_table(table_name)
        table.put_item(Item=item)
        return True
    except Exception as e:
        logger.error(f"Error putting item in {table_name}: {e}")
        return False

def get_item(table_name: str, key: dict) -> Optional[dict]:
    """
    Retrieves a single item by its partition key.
    Returns the item dict or None if not found.

    Usage: get_item("Personas", {"persona_id": "uuid-1234"})
    """
    try:
        table = get_table(table_name)
        response = table.get_item(Key=key)
        return response.get("Item")  # returns None if key "Item" not present
    except Exception as e:
        logger.error(f"Error getting item from {table_name}: {e}")
        return None

def delete_item(table_name: str, key: dict) -> bool:
    """
    Deletes a single item by its partition key.
    Returns True on success, False on failure.

    Usage: delete_item("Personas", {"persona_id": "uuid-1234"})
    """
    try:
        table = get_table(table_name)
        table.delete_item(Key=key)
        return True
    except Exception as e:
        logger.error(f"Error deleting item from {table_name}: {e}")
        return False

def list_items(table_name: str) -> list:
    """
    Returns ALL items in a table using a scan.
    Warning: scan reads every item in the table.
    Fine for small tables, expensive for large ones.
    For production with large tables, use query instead.
    """
    try:
        table = get_table(table_name)
        response = table.scan()
        return response.get("Items", [])
    except Exception as e:
        logger.error(f"Error scanning {table_name}: {e}")
        return []

def update_item(table_name: str, key: dict, updates: dict) -> bool:
    """
    Updates specific fields on an existing item.
    Only the fields in `updates` are changed — everything else stays.

    Usage: update_item("Personas", {"persona_id": "uuid-1234"}, {"tone": "calm"})
    """
    try:
        table = get_table(table_name)

        # Build the UpdateExpression dynamically from the updates dict
        update_expression = "SET " + ", ".join(
            f"#attr_{i} = :val_{i}" for i in range(len(updates))
        )
        expression_names = {
            f"#attr_{i}": key_name
            for i, key_name in enumerate(updates.keys())
        }
        expression_values = {
            f":val_{i}": val
            for i, val in enumerate(updates.values())
        }

        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
        )
        return True
    except Exception as e:
        logger.error(f"Error updating item in {table_name}: {e}")
        return False