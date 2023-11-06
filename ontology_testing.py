# testing.py

# Importing necessary classes and methods from the knowledge_base_module
from knowledge_base_module.entity import Entity
from knowledge_base_module.ontology import Ontology

# Creating an instance of the Ontology class
ontology = Ontology()

# Creating entities
profession = Entity(name="Profession", is_common_noun=True)
journalist = Entity(name="Journalist", is_common_noun=True)
athlete = Entity(name="Athlete", is_common_noun=True)
cricketer = Entity(name="Cricketer", is_common_noun=True)

arnab = Entity(name="Arnab Goswami", is_common_noun=False, attributes={})
rajdeep = Entity(name="Rajdeep Sardesai", is_common_noun=False, attributes={})
sachin = Entity(name="Sachin Tendulkar", is_common_noun=False, attributes={})
rahul = Entity(name="Rahul Dravid", is_common_noun=False, attributes={})

# Adding entities to the ontology
entities = [profession, journalist, athlete, cricketer, arnab, rajdeep, sachin, rahul]
for entity in entities:
    ontology.add_entity(entity)

# Adding relationships
ontology.add_relationship("subtype_of", journalist, profession)
ontology.add_relationship("subtype_of", athlete, profession)
ontology.add_relationship("subtype_of", cricketer, athlete)

ontology.add_relationship("instance_of", arnab, journalist)
ontology.add_relationship("instance_of", rajdeep, journalist)
ontology.add_relationship("instance_of", sachin, cricketer)
ontology.add_relationship("instance_of", rahul, cricketer)

# Adding more instances
journalist.add_instances(['Larry King'], ontology)

# Displaying hierarchical relationships
print("Displaying hierarchical relationship (list):")
ontology.display_hierarchy_list(profession, "has_subtype")

# Optional: If you have implemented a tree structure display
print("\nDisplaying hierarchical relationship (tree):")
ontology.display_hierarchy_tree(profession, "has_subtype")
