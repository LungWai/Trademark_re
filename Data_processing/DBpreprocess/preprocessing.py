import json
import os
from visualizing import JsonViser
from flattenJson import JsonFlattener
from delEmptyAttr import JsonCleaner  # Updated import statement to reflect the class-based approach
from convert import JsonLinesToDynamoDBConverter

class SuperPreprocessor(JsonViser, JsonFlattener, JsonLinesToDynamoDBConverter, JsonCleaner):  # Added JsonCleaner as a parent class
    def __init__(self, input_path, output_path,flatten_outpath, clean_outpath, dynamodb_outpath, k=9):
        self.input_path = input_path
        self.output_path = output_path
        self.flatten_outpath = flatten_outpath
        self.clean_outpath = clean_outpath
        self.dynamodb_outpath = dynamodb_outpath
        self.k = k
        
        # JsonViser.__init__(self, self.input_path, self.output_path, self.k)
        # JsonFlattener.__init__(self, self.output_path, self.flatten_outpath)
        # JsonLinesToDynamoDBConverter.__init__(self, self.clean_outpath, self.dynamodb_outpath)
        # JsonCleaner.__init__(self, self.flatten_outpath, self.clean_outpath)  # Initialized JsonCleaner with output_path for both input and output


    def file_check(self, file):
        if not os.path.exists(file):
            print(f"The file {file} does not exist. Creating a new file.")
            with open(file, 'w', encoding='utf-8') as f:
                f.write("")  # Creates an empty file or initializes as needed



    def preprocess(self):
        self.file_check(self.input_path)
        self.file_check(self.output_path)
        self.file_check(self.flatten_outpath)
        self.file_check(self.clean_outpath)
        self.file_check(self.dynamodb_outpath)

        # Visualize first k JSON lines
        print("Visualizing first k JSON lines...")
        extractor = JsonViser(self.input_path, self.output_path, self.k)
        extractor.get_first_k_jsonlines(write_flag=True)
        # print(f"First {self.k} JSON lines written to", self.output_path)
        
        # Flatten JSON
        print("Flattening JSON...")
        flattener = JsonFlattener(self.output_path, self.flatten_outpath)
        flattener.flatten_json(copy_only=False)
        print("Flattened JSON written to", self.flatten_outpath)

        # Remove empty attributes
        print("Removing empty attributes...")
        cleaner = JsonCleaner(self.flatten_outpath, self.clean_outpath)
        cleaner.clean_json_objects()  # Updated method call to use the class method from JsonCleaner
        print("Empty attributes removed.")

        # Convert to DynamoDB JSON
        print("Converting to DynamoDB JSON format...")
        DB = JsonLinesToDynamoDBConverter(self.clean_outpath, self.dynamodb_outpath)
        DB.convert_jsonlines_to_dynamodb_json()
        print("Conversion complete. DynamoDB JSON written to", 
              self.dynamodb_outpath)

        return None

# Example usage
if __name__ == "__main__":
    input_path = 'Testfile\\trademark5.jsonlines'
    output_path = 'Testfile\\getkTM.jsonlines'
    flatten_outpath = 'Testfile\\flattenTM.jsonlines'
    clean_outpath = 'Testfile\\cleanTM.jsonlines'
    dynamodb_outpath = 'Testfile\\dynamodb.json'
    super_preprocessor = SuperPreprocessor(input_path, output_path,
                                           flatten_outpath, clean_outpath, 
                                           dynamodb_outpath, k=1000)
    super_preprocessor.preprocess()
