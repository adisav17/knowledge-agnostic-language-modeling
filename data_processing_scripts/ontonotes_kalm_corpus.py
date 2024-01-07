

import os
import pandas as pd
import ast

# set path to the data folder
os.chdir('/content/drive/My Drive/kalm/kalm_lm/data')

## see pre-processing notebooks

entity_label_index_to_word = {
    1: "PERSON",       # People's names
    2: "PERSON",       # Also seems to represent people's names, possibly surnames or mononyms
    3: "NORP",         # Nationalities, religious, or political groups
    4: "NORP",         # Nationalities or ethnicities
    5: "FAC",          # Facilities or locations (e.g., 'Disney', 'Bank', 'Center')
    6: "FAC",          # Facilities (e.g., 'Disneyland', 'Ocean Park')
    7: "ORG",          # Organizations, includes media and political parties (e.g., 'Disney', 'CNN', 'KMT')
    8: "ORG",          # Organizations, including governmental and corporate entities
    9: "GPE",          # Geopolitical entities
    10: "GPE",         # Geopolitical entities
    11: "LOC",         # Locations (e.g., 'Lantau', 'Victoria', geographical features)
    12: "LOC",         # Specific locations, geographical features
    13: "VEHICLE",     # Vehicles, ships, and related terms
    14: "VEHICLE",     # Specific vehicles (e.g., 'USS Cole')
    15: "DATE",        # Dates, years, timespans
    16: "DATE",        # Specific years, dates, seasons
    17: "TIME",        # Times of day, hours
    18: "TIME",        # Times, durations, periods of the day
    19: "NUMBER",      # Numbers, including numerical terms
    20: "PERCENT",     # Percentages
    21: "MONEY",       # Monetary values, financial terms
    22: "MONEY",       # Financial amounts, currencies
    23: "QUANTITY",    # Quantities, measurements
    24: "QUANTITY",    # Measurements, sizes, areas
    25: "ORDINAL",     # Ordinal numbers
    26: "DATE",        # Dates, timespans (less specific)
    27: "CARDINAL",    # Cardinal numbers, quantities
    28: "CARDINAL",    # Large numbers, statistical figures
    29: "EVENT",       # Events, incidents, and notable occurrences
    30: "EVENT",       # Events, fairs, exhibitions
    31: "WORK_OF_ART", # Works of art, literature, media titles
    32: "WORK_OF_ART", # Specific works of art, media titles
    33: "LAW",         # Legal documents, laws, legal terms
    34: "LAW",         # Legal acts, laws, constitutional documents
    35: "LANGUAGE"    # Languages, linguistic groups
}

onto_df = pd.read_csv('onto_data_new.csv')

onto_df.head()

## testing

l1 = ast.literal_eval(onto_df['named_entities'][11])

onto_df['words'][11]

for i in range(1,15):

  l1 = ast.literal_eval(onto_df['named_entities'][i])
  l2 = onto_df['words'][i].split()

  print(" ")
  print(i)
  print(l1)
  print(l2)

  for x,y in zip(l1,l2):

    print(x,y)



def create_kalm_corpus_dataframe(df, sentences_column_name, named_entities_column_name):
    def replace_entities(sentence_str, entities):
        sentence = sentence_str.split()  # Split the sentence string into words
        entities = ast.literal_eval(entities)  # Convert string representation of list to actual list
        kalm_sentence = []
        inside_entity = False
        entity_start = 0

        for i, entity in enumerate(entities):
            if entity == 0:
                if inside_entity:
                    # End of entity sequence
                    kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")
                    inside_entity = False
                kalm_sentence.append(sentence[i])  # Add non-entity word
            elif entity % 2 != 0:  # Odd number, beginning of an entity
                if inside_entity:
                    # End previous entity sequence before starting a new one
                    kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")
                inside_entity = True
                entity_start = entity

        # Handle case where sentence ends with an entity
        if inside_entity:
            kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")

        return ' '.join(kalm_sentence)

    # Apply the function to each row
    df['kalm_sentences'] = df.apply(lambda row: replace_entities(row[sentences_column_name], row[named_entities_column_name]), axis=1)
    return df


# df_onto = pd.DataFrame(...)  # Your dataframe here
updated_df = create_kalm_corpus_dataframe(onto_df, 'words', 'named_entities')

updated_df['kalm_sentences'][5]
## more sample testing

i=5002
print(i)
print(updated_df['words'][i])
print(updated_df['words'][i].split(' '))
print(ast.literal_eval(updated_df['named_entities'][i]))
print(" ")
print("current output")
print(updated_df['kalm_sentences'][i])
print(" ")
print("desired output")
print("$ORG 's factoring business works with companies in the apparel , textile and food industries , among others .")


def create_kalm_corpus_dataframe_new(df, sentences_column_name, named_entities_column_name):
    def replace_entities(sentence_str, entities):
        sentence = sentence_str.split()  # Split the sentence string into words
        entities = ast.literal_eval(entities)  # Convert string representation of list to actual list
        kalm_sentence = []
        inside_entity = False
        entity_start = 0

        for i, entity in enumerate(entities):
            if entity == 0:
                if inside_entity:
                    # End of entity sequence
                    entity_str = f"${entity_label_index_to_word[entity_start]}"
                    if i < len(sentence) and sentence[i] == "'s":  # Check for apostrophe 's following the entity
                        entity_str += " 's"
                        i += 1  # Skip the next word as it is part of the entity
                    kalm_sentence.append(entity_str)
                    inside_entity = False
                if i < len(sentence):
                    kalm_sentence.append(sentence[i])  # Add non-entity word
            elif entity % 2 != 0:  # Odd number, beginning of an entity
                if inside_entity:
                    # End previous entity sequence before starting a new one
                    kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")
                inside_entity = True
                entity_start = entity

        # Handle case where sentence ends with an entity
        if inside_entity:
            kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")

        return ' '.join(kalm_sentence)

    # Apply the function to each row
    df['kalm_sentences'] = df.apply(lambda row: replace_entities(row[sentences_column_name], row[named_entities_column_name]), axis=1)
    return df



updated_df_new = create_kalm_corpus_dataframe_new(onto_df, 'words', 'named_entities')


for i in range(0,15):
  print(updated_df_new["kalm_sentences"][i])


def replace_entities(sentence_str, entities_str, entity_label_index_to_word):
    sentence = sentence_str.split()  # Split the sentence string into words
    entities = ast.literal_eval(entities_str)  # Convert string representation of list to actual list
    kalm_sentence = []
    inside_entity = False
    entity_start = 0

    i = 0
    while i < len(entities):
        entity = entities[i]

        if entity == 0:
            if inside_entity:
                # End of entity sequence
                entity_str = f"${entity_label_index_to_word[entity_start]}"
                if i < len(sentence) and sentence[i] == "'s":  # Check for apostrophe 's following the entity
                    entity_str += " 's"
                    i += 1  # Skip the next word as it is part of the entity
                kalm_sentence.append(entity_str)
                inside_entity = False
            if i < len(sentence):
                kalm_sentence.append(sentence[i])  # Add non-entity word
        elif entity % 2 != 0:  # Odd number, beginning of an entity
            if inside_entity:
                # End previous entity sequence before starting a new one
                kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")
            inside_entity = True
            entity_start = entity

        i += 1

    # Handle case where sentence ends with an entity
    if inside_entity:
        kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")

    return ' '.join(kalm_sentence)



def create_kalm_corpus_dataframe_gamma(df, sentences_column_name, named_entities_column_name):
    def replace_entities(sentence_str, entities):
        sentence = sentence_str.split()  # Split the sentence string into words
        entities = ast.literal_eval(entities)  # Convert string representation of list to actual list
        kalm_sentence = []
        inside_entity = False
        entity_start = 0

        for i, entity in enumerate(entities):
            if entity == 0:
                if inside_entity:
                    # End of entity sequence

                    # check if it ends with 's
                    if(len(sentence)>i and sentence[i-1] == " 's"):

                      kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")
                      kalm_sentence.append(" 's")

                    # else append as normal
                    else:
                       kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")

                    inside_entity = False
                kalm_sentence.append(sentence[i])  # Add non-entity word
            elif entity % 2 != 0:  # Odd number, beginning of an entity
                if inside_entity:
                    # End previous entity sequence before starting a new one
                    kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")
                inside_entity = True
                entity_start = entity

        # Handle case where sentence ends with an entity
        if inside_entity:
            kalm_sentence.append(f"${entity_label_index_to_word[entity_start]}")

        return ' '.join(kalm_sentence)

    # Apply the function to each row
    df['kalm_sentences'] = df.apply(lambda row: replace_entities(row[sentences_column_name], row[named_entities_column_name]), axis=1)
    return df

# Example usage
# df_onto = pd.DataFrame(...)  # Your dataframe here
# updated_df = create_kalm_corpus_dataframe(df_onto, 'words', 'named_entities')

updated_df_gamma = create_kalm_corpus_dataframe(onto_df, 'words', 'named_entities')

updated_df = updated_df_gamma

updated_df.head()

kalm_df = updated_df.copy()

kalm_df = kalm_df.drop(index=2)

kalm_df = kalm_df.drop(columns=['Unnamed: 0', 'named_entities'])

kalm_df = kalm_df.rename(columns={'words': 'sentences'})

print(os.getcwd())

kalm_df.head()

kalm_df.to_csv('kalmified_corpus_ontonotes.csv', index=False)

### save ontonotes_calmified_corpus 

def count_unique_words_per_column(df, column_names):
    unique_word_counts = {}
    total_word_counts = {}
    for column in column_names:
        unique_words = set()
        total_words = 0
        for sentence in df[column]:
            words = sentence.split()
            unique_words.update(words)
            total_words += len(words)-1

        unique_word_counts[column] = len(unique_words)
        total_word_counts[column] = total_words

    return unique_word_counts, total_word_counts

# Example usage
# Assuming kalm_df is your DataFrame and it has columns 'sentences' and 'kalm_sentences'
column_names = ['sentences', 'kalm_sentences']
unique_word_count_dict, total_word_count_dict = count_unique_words_per_column(kalm_df, column_names)
print("Unique word count per column:")
for column, count in unique_word_count_dict.items():
    print(f"{column}: {count}")




### corpus reduction
