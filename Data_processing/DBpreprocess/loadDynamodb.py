import boto3
from boto3.session import Session
import json
from botocore.exceptions import ClientError

def load_json_to_dynamodb(json_file_path, dynamodb_client, TableName):
    print("Starting upload to DynamoDB...")
    with open(json_file_path, 'r') as file:
        for line in file:
            if line.strip():  # make sure line is not empty
                item = json.loads(line)
                try:
                    response = dynamodb_client.put_item(TableName=TableName, Item=item['M'])
                    # print("Item successfully added:", item)
                except ClientError as e:
                    print("Error adding item:", e.response['Error']['Message'])
    print("Upload to DynamoDB completed.")


def verify_first_five_items(table):
    print("Verifying the first five items in the table...")
    response = table.scan(Limit=5)
    items = response['Items']
    if items:
        print("First five items for verification:")
        for item in items:
            print(item)
    else:
        print("No items found for verification.")
    print("Verification completed.")

def create_dynamodb_table(dynamodb_res, table_name, partition_key, sort_key=None):
    # Define the primary key schema
    key_schema = [
        {
            'AttributeName': partition_key,
            'KeyType': 'HASH'  # Partition key
        }
    ]
    attribute_definitions = [
        {
            'AttributeName': partition_key,
            'AttributeType': 'S'  # String type
        }
    ]
    # If a sort key is provided, add it to the schema
    if sort_key:
        key_schema.append({
            'AttributeName': sort_key,
            'KeyType': 'RANGE'  # Sort key
        })
        attribute_definitions.append({
            'AttributeName': sort_key,
            'AttributeType': 'S'  # Assuming string type for simplicity
        })

    # Create the table
    table = dynamodb_res.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        BillingMode='PAY_PER_REQUEST'  # On-demand pricing
    )

    # Wait until the table exists, this will block until AWS confirms table creation
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table {table_name} created successfully.")


def test_dynamodb_insert(dynamodb_client, TableName):
    item = {
        "id": {"S": "1"},
        "name": {"S": "John Doe11"},
        "email": {"S": "john@example.com"}
    }
    try:
        response = dynamodb_client.put_item(TableName=TableName, Item=item)
        print("Item successfully added:", item)
    except Exception as e:
        print(f"Failed to add item: {item}. Error: {e}")


if __name__ == "__main__":
    json_file_path = 'trademark5\\dynamodb.json'
    
    print("Establishing session with DynamoDB...")
    session = Session(profile_name='uploader')
    dynamodb_res = session.resource('dynamodb', region_name='us-east-1')
    dynamodb_cli = session.client('dynamodb', region_name='us-east-1')
    
    flag = 0

    # flag = 1 is test ExampleTable; create and insert
    # flag = 2 is tset table TestTM_10ea; create and insert from json
    # flag = 3 is verify table TestTM_10ea
    # flag = 0; custom your table insert at this condition

    if flag==1:
        create_dynamodb_table(dynamodb_res, 'ExampleTable', 'id')
        test_dynamodb_insert(dynamodb_cli, 'ExampleTable')
    elif flag ==2:
        create_dynamodb_table(dynamodb_res, 'TestTM_10ea', 'status', 'id')
        load_json_to_dynamodb(json_file_path, dynamodb_cli, 'TestTM_10ea')
    elif flag == 3:
        table = dynamodb_res.Table('TestTM_10ea')
        verify_first_five_items(table)
    elif flag == 0:
        # custom your table insert at this condition
        json_file_path = 'Datafile\\dynamodb.json'
        Table_name = 'TestTM_1000ea'
        p_key = 'status'
        s_key = 'id'
        create_dynamodb_table(dynamodb_res, Table_name, partition_key= p_key, sort_key= s_key)
        load_json_to_dynamodb(json_file_path, dynamodb_cli, Table_name)
    else:
        print("invalid input flag")
        