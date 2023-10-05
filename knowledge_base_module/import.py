class DataImport:
    def __init__(self, folder_path, metadata_file):
        self.folder_path = folder_path
        self.metadata_file = metadata_file

    def import_entities(self, ontology):
        # logic to read entities from terminal folders and add to the ontology
        pass

    def import_relationships(self, ontology):
        # logic to read metadata file and establish relationships in the ontology
        pass

    def validate_structure(self):
        # logic to validate folder structure and metadata file format
        pass
