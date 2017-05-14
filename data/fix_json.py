import json
import glob


def load_json(filename):
    with open(filename, encoding='utf8') as f:
        return [json.loads(line) for line in f]


def dump_json(data, filename):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f)


json_files = glob.glob('*.json')

for json_file in json_files:
    data = load_json(json_file)
    dump_json(data, json_file)
