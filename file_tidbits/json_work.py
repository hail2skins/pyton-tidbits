import json

def read_print_json(file, pretty, sort):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        if pretty:
            print(json.dumps(data, indent=4, sort_keys=sort))
        else:
            print(data)
            
def update_author_json(file, arr_name, pos, key, value):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        data[arr_name][pos][key] = value
    with open(file, 'w') as write_file:
        json.dump(data, write_file, indent=4, sort_keys=True)
        
#read_print_json('./file_tidbits/files_to_read/authors.json', True, True)

update_author_json('./file_tidbits/files_to_read/authors.json', 'authors', 1, 'courses', 5)





