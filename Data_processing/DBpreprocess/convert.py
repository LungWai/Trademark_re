import json

class JsonLinesToDynamoDBConverter:
    def __init__(self, jsonlines_file, dynamodb_json_file):
        """
        Initializes the converter with paths to the input .jsonl file and the output file for DynamoDB-formatted JSON objects.

        :param jsonlines_file: Path to the input .jsonl file.
        :param dynamodb_json_file: Path to the output file, which will contain the DynamoDB-formatted JSON objects.
        """
        self.jsonlines_file = jsonlines_file
        self.dynamodb_json_file = dynamodb_json_file

    def convert_jsonlines_to_dynamodb_json(self):
        """
        Converts a .jsonl file to a format suitable for DynamoDB and writes the output to a new file.

        Each line in the input file is expected to be a valid JSON object. The function transforms each JSON object
        into a DynamoDB-compatible format, where each attribute's value is a dictionary specifying its type and value.
        """
        with open(self.jsonlines_file, 'r', encoding='utf-8') as infile, open(self.dynamodb_json_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                try:
                    item = json.loads(line.strip())
                    dynamodb_item = self.convert_to_dynamodb_json(item)
                    outfile.write(json.dumps(dynamodb_item) + '\n')
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    print(f"Problematic line: {line}")

    def convert_to_dynamodb_json(self, item):
        """
        Converts a Python dictionary to a DynamoDB-compatible JSON format.

        :param item: A Python dictionary representing a single item, or any value to be converted.
        :return: A dictionary formatted for DynamoDB.
        """
        # If the item is a dictionary, process each key-value pair
        if isinstance(item, dict):
            dynamodb_item = {'M': {}}
            for attr, value in item.items():
                dynamodb_item['M'][attr] = self.convert_to_dynamodb_json(value)
            return dynamodb_item
        # If the item is a list, process each element
        elif isinstance(item, list):
            return {'L': [self.convert_to_dynamodb_json(elem) for elem in item]}
        # If the item is a string, return it as a DynamoDB string type
        elif isinstance(item, str):
            return {'S': item}
        # If the item is an integer or float, return it as a DynamoDB number type
        elif isinstance(item, (int, float)):
            return {'N': str(item)}
        # Add more type checks as necessary
        else:
            # Skip or handle other types as needed
            return None

# Example usage
if __name__ == "__main__":
    jsonlines_file = 'trademark5/cleaned_fewLine.jsonlines'
    dynamodb_json_file = 'trademark5/test_dynamodb.json'
    converter = JsonLinesToDynamoDBConverter(jsonlines_file, dynamodb_json_file)
    converter.convert_jsonlines_to_dynamodb_json()
