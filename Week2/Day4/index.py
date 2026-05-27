import json
import os
from pathlib import Path
my_family = {
    "firstName": "Jane",
    "lastName": "Doe",
    "hobbies": ["running", "sky diving", "singing"],
    "age": 35,
    "children": [
        {
            "firstName": "Alice",
            "age": 6
        },
        {
            "firstName": "Bob",
            "age": 8
        }
    ]
}

current_folder = Path(__file__).parent
file_path = current_folder / "file.json"
with open(file_path, 'w') as file_obj:
    json.dump(my_family, file_obj, indent=2, sort_keys=True)
    
print("File written here:")
print(os.getcwd())


with open(file_path, 'r') as file_obj:
    family = json.load(file_obj)
print(family)

colors = ["blue", "brown"]
for child, color in zip(family["children"], colors):
    child["favorite_color"] = color

print(family)