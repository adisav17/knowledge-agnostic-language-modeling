class Entity:
    def __init__(self, name, is_common_noun = False, attributes=None):
        self.name = name
        self.is_common_noun = is_common_noun
        self.attributes = attributes if attributes else {}
        self.relationships = {}

    def add_relationship(self, relation_type, related_entity):
        self.relationships.setdefault(relation_type, set()).add(related_entity.name)

    
    def get_instances(self, relation_type='has_instance'):
        return list(self.relationships.get(relation_type, []))     

    def add_instances(self, instances, ontology, relation_type='has_instance', is_common_noun=False):
        if not isinstance(instances, list):
            instances = [instances]  # If a single instance is provided, convert it to a list

        for instance_name in instances:
            instance_entity = ontology.entities.get(instance_name)
            if not instance_entity:
                instance_entity = Entity(name=instance_name, is_common_noun=is_common_noun)  # Create new entity if not found
                ontology.add_entity(instance_entity)  # Add the new entity to the ontology
                print(f"Entity {instance_name} created and added to the ontology.")
                
            self.add_relationship(relation_type, instance_entity)     

    def __str__(self):
        return self.name
