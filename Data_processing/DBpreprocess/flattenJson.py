import json

class JsonFlattener:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def flatten_json(self, copy_only=False):
        if copy_only:
            with open(self.input_path, 'r') as f, open(self.output_path, 'w') as out_f:
                for line in f:
                    out_f.write(line)
        else:
            with open(self.input_path, 'r') as f, open(self.output_path, 'w') as out_f:
                first_object = True
                for line in f:
                    data = json.loads(line)  # Parse each line as a separate JSON object
                    flat_data = self._flatten(data)  # Flatten the JSON object
                    if not first_object:
                        # For all but the first object, prepend a newline to separate objects
                        out_f.write('\n')
                    else:
                        first_object = False
                    json.dump(flat_data, out_f)  # Write the flattened object as a JSON string without newlines between attributes

    def _flatten(self, y, name='', out=None, skip_key="specifications"):
        if out is None:
            out = {}
        if isinstance(y, dict):
            for a in y:
                if a == skip_key:  # Check if the key matches the skip_key
                    out[name[:-1] + a] = y[a]  # Do not flatten this dictionary
                else:
                    self._flatten(y[a], name + a + '_', out, skip_key)
        elif isinstance(y, list):
            for i, a in enumerate(y):
                self._flatten(a, name + str(i) + '_', out, skip_key)
        else:
            out[name[:-1]] = y
        return out





# Example usage
if __name__ == '__main__':
    flattener = JsonFlattener('trademark5\\fewLine.jsonlines', 'trademark5\\flattened_fewLine.jsonlines')
    flat_data = flattener.flatten_json()
