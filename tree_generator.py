from data_fetch import *
import json
from json import JSONEncoder

FILE_NAME="tree_structure.json"

TREE_FILE_NAME = os.path.join(PATH, FILE_NAME) 

class Node(object):
    def __init__(self, name, values=None):
        self.name = name
        if values != None:
            self.values = values
        else:
            self.values = []
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
# subclass JSONEncoder
class EmployeeEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

            
if __name__ == '__main__':

    cache_file = open(DATA_FILE_NAME, 'r')
    cache_file_contents = cache_file.read()
    Data_dict = json.loads(cache_file_contents)
    cache_file.close()
    root = Node('continent');
    continent = Data_dict.keys()
    for continent_name in continent:
        continent_node = Node(continent_name)

        country_list = Data_dict[continent_name]
        country = country_list.keys()

        for country_name in country:
            country_node = Node(country_name)
            
            lake_list = country_list[country_name]
            lake = lake_list.keys()
            
            for lake_name in lake_list:
                data = lake_list[lake_name]
                lake_node = Node(lake_name, data)
                country_node.add_child(lake_node)
            continent_node.add_child(country_node)

        root.add_child(continent_node)
            
    cache_file = open(TREE_FILE_NAME, 'w')
    contents_to_write = json.dumps(root, indent=4, cls=EmployeeEncoder)
    cache_file.write(contents_to_write)
    cache_file.close()

