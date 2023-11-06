class Relationship:
    def __init__(self, relation_type, entity1, entity2):
        self.relation_type = relation_type
        self.entity1 = entity1
        self.entity2 = entity2
        entity1.add_relationship(relation_type, entity2)
        entity2.add_relationship(self.inverse_relation(relation_type), entity1)

    def inverse_relation(self, relation_type):
        # This method returns the inverse of the relation type.
        # For simplicity, we'll use a dictionary. This should be expanded upon.
        inverse_relations = {
            "subtype_of": "has_subtype",
            "instance_of": "has_instance"
        }
        return inverse_relations.get(relation_type, f"related_to_{relation_type}")
