import os
import os
import json

## given a populated ontology, populate the folder structure in the designated path 

class DataExport:
    def __init__(self, folder_path, metadata_file):
        self.folder_path = folder_path
        self.metadata_file = metadata_file

    def export_entities(self, ontology):
        for entity_name, entity in ontology.entities.items():
            entity_path = os.path.join(self.folder_path, entity_name)
            os.makedirs(entity_path, exist_ok=True)

            if 'has_instance' in entity.relationships:
                with open(os.path.join(entity_path, 'instances.txt'), 'w') as file:
                    for instance in entity.relationships['has_instance']:
                        file.write(instance + '\n')

            if 'has_subtype' in entity.relationships:
                for subtype in entity.relationships['has_subtype']:
                    subtype_entity = ontology.entities.get(subtype)
                    if subtype_entity:
                        self._export_subtypes(entity_path, subtype_entity, ontology)

    def _export_subtypes(self, parent_path, entity, ontology):
        entity_path = os.path.join(parent_path, entity.name)
        os.makedirs(entity_path, exist_ok=True)

        if 'has_instance' in entity.relationships:
            with open(os.path.join(entity_path, 'instances.txt'), 'w') as file:
                for instance in entity.relationships['has_instance']:
                    file.write(instance + '\n')

        if 'has_subtype' in entity.relationships:
            for subtype in entity.relationships['has_subtype']:
                subtype_entity = ontology.entities.get(subtype)
                if subtype_entity:
                    self._export_subtypes(entity_path, subtype_entity, ontology)

    def export_entities(self, ontology):
        # logic to export entities from ontology to terminal folders
        pass

    def export_relationships(self, ontology):
        # logic to write relationships from ontology to metadata file
        pass

    def create_structure(self):
        # logic to create folder structure for exporting data
        pass

    def update_folder_structure(self, ontology):
        # Removes existing folder structure and recreates it based on the updated ontology
        # This could be optimized to only update the changed parts
        pass
