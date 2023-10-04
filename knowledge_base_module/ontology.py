import entity, relationship
from relationship import Relationship
from entity import Entity

class Ontology:
    def __init__(self):
        self.entities = {}

    def add_entity(self, entity):
        if entity.is_common_noun:
            self.entities[entity.name] = entity
        else:
            print(f"Entity {entity.name} is not a common noun entity and can't be added to ontology.")

    def add_relationship(self, relation_type, entity1, entity2):
        #if entity1.is_common_noun and entity2.is_common_noun:
            Relationship(relation_type, entity1, entity2)
        #else:
        #    print(f"One or both entities are not common noun entities.")


    def get_hierarchy_list(self, entity, relation_type, hierarchy=None, visited=None):
        if hierarchy is None:
            hierarchy = []
        if visited is None:
            visited = set()

        if entity.name in visited:
            return hierarchy
        visited.add(entity.name)

        if relation_type in entity.relationships:
            for related_entity_name in entity.relationships[relation_type]:
                hierarchy.append(related_entity_name)
                related_entity = self.entities.get(related_entity_name)  # Fetch the actual entity object
                if related_entity:  # If the entity exists
                    self.get_hierarchy_list(related_entity, relation_type, hierarchy, visited)

        return hierarchy 

    

    def get_hierarchy_tree(self, entity, relation_type, visited=None):
        
        hierarchy = []
        if visited is None:
            visited = set()

        if entity.name in visited:
            return hierarchy
        visited.add(entity.name)

        if relation_type in entity.relationships:
            for related_entity_name in entity.relationships[relation_type]:
                hierarchy.append(related_entity_name)
                related_entity = self.entities.get(related_entity_name)  # Fetch the actual entity object
                if related_entity:  # If the entity exists
                   # self.get_hierarchy(related_entity, relation_type, hierarchy, visited)
                   branch = self.get_hierarchy_tree(related_entity,relation_type,visited)
                   if branch is not None:
                       hierarchy.append(branch)


        return hierarchy    
    


    def search_entities(self, criteria):
        # Placeholder for a method that will search entities based on provided criteria
        pass

    def update_relationship(self, entity, old_relation, new_relation):
        # Placeholder for a method to update relationships
        pass

    def delete_relationship(self, entity, relation_type):
        # Placeholder for a method to delete relationships
        pass

    def validate_entity(self, entity):
        # Placeholder for a method to validate entities before addition
        pass

    def visualize(self):
        # Placeholder for a method to visualize the ontology
        pass

    def export_ontology(self, format):
        # Placeholder for a method to export ontology to a specific format
        pass

    def import_ontology(self, data, format):
        # Placeholder for a method to import ontology from a specific format
        pass

    def display_hierarchy_list(self, entity, relation_type):
        hierarchy = self.get_hierarchy_list(entity, relation_type)
        print(" > ".join(reversed(hierarchy)) + f" > {entity.name}")

    def display_hierarchy_tree(self, entity, relation_type, indent=0):

        hierarchy_tree = self.get_hierarchy_tree(entity, relation_type)
        self._print_tree(hierarchy_tree, indent)

    def _print_tree(self, tree, indent): 
        for item in tree:
            if isinstance(item, list):
                self._print_tree(item, indent + 2)
            else:
                print(' ' * indent + '- ' + item)





    
