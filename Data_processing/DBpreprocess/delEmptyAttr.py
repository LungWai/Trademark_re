import json

class JsonCleaner:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def clean_json_objects(self):
        # Initialize a list to hold the cleaned JSON objects
        cleaned_objects = []
        
        # Read the entire content of the .jsonlines file
        with open(self.input_file_path, 'r') as file:
            json_object_str = ''
            for line in file:
                stripped_line = line.strip()
                if stripped_line:  # Check if the line is not empty
                    json_object_str += stripped_line
                if stripped_line.endswith('}'):  # Check if the line ends with a closing brace
                    # Parse the accumulated string as a JSON object
                    try:
                        json_object = json.loads(json_object_str)
                        # Remove keys with None values
                        cleaned_json_object = {k: v for k, v in json_object.items() if v is not None}
                        cleaned_objects.append(cleaned_json_object)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON object: {e}")
                    finally:
                        json_object_str = ''  # Reset for the next object

        # Write the cleaned JSON objects to a new file
        with open(self.output_file_path, 'w') as cleaned_file:
            for obj in cleaned_objects:
                cleaned_json_str = json.dumps(obj)
                cleaned_file.write(cleaned_json_str + '\n')

# Example usage
if __name__ == '__main__':
    input_file_path = 'trademark5/flattened_fewLine.jsonlines'
    output_file_path = 'trademark5/cleaned_fewLine.jsonlines'
    cleaner = JsonCleaner(input_file_path, output_file_path)
    cleaner.clean_json_objects()
