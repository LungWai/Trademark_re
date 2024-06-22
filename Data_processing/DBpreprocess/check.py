import json
import os

class JsonlFileChecker:
    def __init__(self, jsonl_file_path, oversized_output_path, line_sizes_output_path, max_line_size_kb=380):
        self.jsonl_file_path = jsonl_file_path
        self.oversized_output_path = oversized_output_path
        self.line_sizes_output_path = line_sizes_output_path
        self.max_line_size_kb = max_line_size_kb

    def get_json_line_size(self, line):
        return len(line.encode("utf-8"))

    def check_jsonl_file(self):
        oversized_lines = []
        line_sizes = []  
        with open(self.jsonl_file_path, "r") as jsonl_file:
            for line_number, line in enumerate(jsonl_file, start=1):
                line_size_kb = self.get_json_line_size(line) / 1024
                if line_size_kb > self.max_line_size_kb:
                    oversized_lines.append(line_number)
                line_sizes.append((line_number, line_size_kb))  

        return oversized_lines, line_sizes  

    def write_line_numbers_to_file(self, line_numbers):
        with open(self.oversized_output_path, "w") as txt_file:
            for line_number in line_numbers:
                txt_file.write(f"{line_number}\n")

    def write_line_sizes_to_file(self, line_sizes):
        with open(self.line_sizes_output_path, "w") as txt_file:
            for line_number, line_size in line_sizes:
                txt_file.write(f"Line {line_number}: {line_size:.2f} KB\n")  

if __name__ == "__main__":
    checker = JsonlFileChecker("trademark5\\trademark5.jsonlines", 
                               "oversized_lines.txt", "line_sizes.txt")
    oversized_line_numbers, line_sizes = checker.check_jsonl_file()  
    checker.write_line_numbers_to_file(oversized_line_numbers)
    checker.write_line_sizes_to_file(line_sizes)  

    print(f"Oversized lines written to {checker.oversized_output_path}.")
    print(f"Line sizes written to {checker.line_sizes_output_path}.")  
    print(f"Total number of oversized lines: {len(oversized_line_numbers)}")

