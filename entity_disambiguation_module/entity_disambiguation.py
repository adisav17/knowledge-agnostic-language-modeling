class EntityDisambiguation:
    def __init__(self, input_text_data, recognized_entities, ontology):
        self.input_text_data = input_text_data
        self.recognized_entities = recognized_entities[0]  # Adjust the index, based on data structure from entity recogniton module, huggingface api
        self.ontology = ontology

    def associate_entities_with_sentences(self):
        entities_in_text = []

        for i, sentence in enumerate(self.input_text_data):
            sentence_entities = []

            for entity in self.recognized_entities:
                if entity['start'] >= len(sentence):

                    break

                sentence_entities.append(entity)
                self.recognized_entities = self.recognized_entities[1:]  # Move to the next entity

            entities_in_text.append(sentence_entities)

        return entities_in_text

    def enrich_entities_with_ontology(self, entities_in_text):
        enriched_entities = []

        for sentence_entities in entities_in_text:
            enriched_sentence_entities = []
            
            for entity in sentence_entities:
                entity_name = entity['word']
                ontology_entity = self.ontology.entities.get(entity_name)

                if ontology_entity and 'instance_of' in ontology_entity.relationships:
                    entity_type_info = ontology_entity.relationships['instance_of']
                    entity['entity_type'] = entity_type_info[0] if entity_type_info else None

                enriched_sentence_entities.append(entity)
            
            enriched_entities.append(enriched_sentence_entities)

        return enriched_entities

    def disambiguate_entities(self):
        entities_in_text = self.associate_entities_with_sentences()
        enriched_entities = self.enrich_entities_with_ontology(entities_in_text)
        return enriched_entities


# - input_text_data: the original text data as a list of sentences
# - reocgnized_entities: the recognized entities from the NER model
# - ontology: the populated ontology object
#  returns entities with categorical entity type information

#disambiguation = EntityDisambiguation(input_text_data, recognized_entities, ontology)
#enriched_entities = disambiguation.disambiguate_entities()
