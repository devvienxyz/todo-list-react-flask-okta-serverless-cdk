import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from utils.logger import logger


class DDBClient:

    def __init__(self, table_name: str, region_name="ap-southeast-1"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def query_items_by_expression(self, key: str, eq_value: str):
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key(key).eq(eq_value)
        )
        return response.get("Items", [])

    def list_items_by_attribute(self, attribute_name, attribute_value, index_name=None):
        try:
            if index_name:
                response = self.table.query(
                    IndexName=index_name,  # Use GSI if querying by an attribute not part of the primary key
                    KeyConditionExpression=Key(attribute_name).eq(attribute_value),
                )
            else:
                response = self.table.query(
                    KeyConditionExpression=Key(attribute_name).eq(attribute_value)
                )

            items = response.get("Items", [])
            logger.exception(f"Items where {attribute_name} = {attribute_value}:", items)
            return items
        except ClientError as e:
            logger.exception(f"Error listing items: {e.response['Error']['Message']}")
            return []

    def patch_item(self, key, update_attributes):
        try:
            update_expression = "SET " + ", ".join(
                f"{k} = :{k}" for k in update_attributes.keys()
            )
            expression_attribute_values = {
                f":{k}": v for k, v in update_attributes.items()
            }

            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW",
            )
            logger.exception("Item successfully updated:", response)
            return response
        except ClientError as e:
            logger.exception(f"Error updating item: {e.response['Error']['Message']}")
            return None

    def delete_item(self, key):
        try:
            response = self.table.delete_item(Key=key)
            logger.exception("Item successfully deleted:", response)
            return response
        except ClientError as e:
            logger.exception(f"Error deleting item: {e.response['Error']['Message']}")
            return None

    def get_item_by_key(self, key):
        try:
            response = self.table.get_item(Key=key)
            item = response.get("Item")
            if item:
                logger.exception("Item retrieved successfully:", item)
                return item
            else:
                logger.exception("Item not found")
                return None
        except ClientError as e:
            logger.exception(f"Error getting item: {e.response['Error']['Message']}")
            return None

    def add_item(self, item):
        try:
            response = self.table.put_item(Item=item)
            logger.exception("Item successfully added:", response)
            return response
        except ClientError as e:
            logger.exception(f"Error adding item: {e.response['Error']['Message']}")
            return None
