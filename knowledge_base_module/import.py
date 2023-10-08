
import json
import os
from knowledge_base_module.entity import Entity

## for a given folder structure and metadata, populate the ontology

class DataImport:
    def __init__(self, folder_path, metadata_file):
        self.folder_path = folder_path
        self.metadata_file = metadata_file


    def _import_entity(self, entity_name, ontology, entity_data, relationship_type, path):
        entity = Entity(name=entity_name, is_common_noun=True)
        ontology.add_entity(entity)

        if not entity_data:  # If it's a terminal node, read instance names from the folder
            instance_names = os.listdir(path)  #  get the actual names of the folders/files
            for instance_name in instance_names:
                instance = Entity(name=instance_name, is_common_noun=False)
                ontology.add_entity(instance)
                ontology.add_relationship("instance_of", instance, entity)
        else:  # If it's a non-terminal node with subtypes
            for subtype_name, subtype_data in entity_data.items():
                subtype_path = os.path.join(path, subtype_name)
                self._import_entity(subtype_name, ontology, subtype_data, relationship_type, subtype_path)

        return entity

    def import_entities(self, ontology):
        with open(self.metadata_file, 'r') as file:
            metadata = json.load(file)
            relationship_type = metadata['relationshipType']

            for entity_name, entity_data in metadata['entities'].items():
                path = os.path.join(self.folder_path, entity_name)
                self._import_entity(entity_name, ontology, entity_data, relationship_type, path)


    def import_relationships(self, ontology):
        # logic to read metadata file and establish relationships in the ontology
        pass

    def validate_structure(self):
        # logic to validate folder structure and metadata file format
        pass
