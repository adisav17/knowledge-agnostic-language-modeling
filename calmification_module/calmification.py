class Calmification:
    def __init__(self, input_text_data, enriched_entities):
        self.input_text_data = input_text_data
        self.enriched_entities = enriched_entities

    def transform_text(self):
        transformed_input_data = []

        for i, sentence in enumerate(self.input_text_data):
            for entity in self.enriched_entities[i]:
                # Replacing entity with entity_type preceded by $
                entity_type = entity.get('entity_type')
                if entity_type:
                    sentence = sentence.replace(entity['word'], f"${entity_type}")

            transformed_input_data.append(sentence)

        return transformed_input_data


#input_text_data = [
#    "Sachin Tendulkar is a good man.", "Arnab is a good man."]
#enriched_entities = [[{"word": "Sachin Tendulkar", "entity_type": "Cricketer"}], [
#    {"word": "Arnab", "entity_type": "Journalist"}]]

#transformed_input_data = ['$Cricketer is a good man.', '$Journalist is a good man.']