import json

## to be expanded
## replicative of folder structure
## write code to adjust metadata dynamically given a folder path

metadata = {
    "relationshipType": "is_subtype",
    "entities": {
        "Professional": {
            "Journalist": {},
            "Engineer": {}
        },
        "Place": {
            "Country": {
                "India": {},
                "USA": {}
            }
        }
    }
}

# Specify the file path; it can be absolute or relative
file_path = 'metadata.json'

# Writing metadata to a JSON file
with open(file_path, 'w') as file:
    json.dump(metadata, file, indent=4)
