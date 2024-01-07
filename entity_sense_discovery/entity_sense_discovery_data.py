

import os
os.chdir('/content/drive/My Drive/kalm/kalm_lm/entity_sense_discovery')

import pandas as pd
import ast
import json
from collections import defaultdict

class Entity_Sense_Discovery_Data:
    def __init__(self, file_path = None):
        self.dataframe_file_path = file_path
        self.df = None
        self.entity_sentences = defaultdict(list)


    def load_data(self):
    
        self.df = pd.read_csv(self.dataframe_file_path)

    def create_entity_sentence_map(self):
        
        for _, row in self.df.iterrows():
            entity_list = ast.literal_eval(row['named_entities'])
            words = row['words'].split()

            for word, entity_tag in zip(words, entity_list):
                if entity_tag != 0:
                    entity_word = word.lower()
                    self.entity_sentences[entity_word].append(row['words'])

    def get_sentences_for_word(self, word):
    
        return self.entity_sentences.get(word.lower(), [])

    def save_to_json(self, output_file_path):
        
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.entity_sentences, file, ensure_ascii=False, indent=4)

    def load_from_json(self, input_file_path):
        
        with open(input_file_path, 'r', encoding='utf-8') as file:
            self.entity_sentences = json.load(file)

    def add_data_from_dataframe(self, new_df):
        
        for _, row in new_df.iterrows():
            entity_list = ast.literal_eval(row['named_entities'])
            words = row['words'].split()

            for word, entity_tag in zip(words, entity_list):
                if entity_tag != 0:
                    entity_word = word.lower()
                    self.entity_sentences[entity_word].append(row['words'])

    def add_data_from_dict(self, new_dict):
        """Add data from another dictionary to the entity_sentences map."""
        for word, sentences in new_dict.items():
            self.entity_sentences[word.lower()].extend(sentences)



# Example usage
file_path = '/content/drive/My Drive/kalm/kalm_lm/data/onto_data_new.csv'
entity_sense_discovery_data = Entity_Sense_Discovery_Data(file_path)
entity_sense_discovery_data.load_data()
entity_sense_discovery_data.create_entity_sentence_map()


#testing 
list(entity_sense_discovery_data.entity_sentences.keys())[:10]

aug_word_sense_dict = {

     "apple": [
         # as fruit, as company in corpus
        "She added chopped apples to the salad.",
        "An apple a day keeps the doctor away.",
        "He picked a ripe apple from the tree.",
        "The apple pie had a delightful cinnamon aroma.",
        "They went apple picking in the orchard.",
        "Her favorite snack is a sliced apple with peanut butter.",
        "The recipe calls for two Granny Smith apples.",
        "She packed a sandwich and an apple for lunch.",
        "Apple juice is his beverage of choice for breakfast.",
        "The apples in the basket were fresh and juicy.",
        "He learned to juggle using three apples.",
        "The kitchen was filled with the scent of apple crumble baking.",
        "She taught the kids how to make apple sauce.",
        "The apple turnover was a perfect dessert.",
        "The apple blossoms in spring are a beautiful sight.",
    ],
    "amazon": [
        # Amazon as a company
        "I ordered a new book from Amazon last night.",
        "Amazon's headquarters are located in Seattle.",
        "She found competitive prices on Amazon for electronics.",
        "Amazon Prime offers fast delivery options.",
        "The company's growth has been a significant part of Amazon's success.",
        "They streamed the movie on Amazon Prime Video.",

        # Amazon as a forest
        "The Amazon rainforest is the largest tropical rainforest in the world.",
        "Many unique species of plants and animals are found in the Amazon.",
        "Deforestation in the Amazon has environmental impacts worldwide.",
        "The Amazon basin spans several South American countries.",
        "Indigenous tribes have been living in the Amazon for thousands of years.",
        "The Amazon rainforest is vital for global oxygen production.",
        "Exploring the Amazon can be a remarkable adventure.",
        "The biodiversity in the Amazon is unparalleled.",
        "Several rivers in South America flow into the Amazon.",
        "The Amazon is known for its incredible natural beauty."
    ],

         "mouse": [
        # Mouse as an animal
        "The small mouse scurried across the kitchen floor.",
        "Cats are natural predators of the mouse.",
        "She saw a mouse peeking out from behind the cupboard.",
        "The mouse nibbled on a piece of cheese.",
        "In the wild, a mouse can be a vital part of the ecosystem.",
        "They set a humane trap to catch the mouse in their home.",
        "The field mouse is common in rural areas.",
        "A mouse's diet mainly consists of seeds and nuts.",
        "Children's stories often feature a mouse as a clever character.",
        "She was startled by a mouse running across the path.",

        # Mouse as a computer device
        "He bought a new wireless mouse for his computer.",
        "Drag and drop the file using the mouse.",
        "The mouse pointer moved erratically on the screen.",
        "She preferred using a mouse over the laptop's touchpad.",
        "Gaming mice often have additional buttons for better control.",
        "Her new mouse had customizable RGB lighting.",
        "The ergonomic mouse reduced strain on her wrist.",
        "A mouse pad can improve the sensor's accuracy.",
        "He configured the mouse settings for faster scrolling.",
        "The Bluetooth mouse connected seamlessly to her computer."
    ],

    "spring": [
        # Spring as a season
        "The flowers bloom beautifully during the spring.",
        "Spring is often associated with renewal and growth.",
        "They planned a picnic to enjoy the spring weather.",
        "The spring equinox occurs around March 20th.",
        "After a long winter, the warmth of spring is welcomed.",
        "Spring break is a popular holiday time for students.",
        "Rain showers are common in the spring months.",
        "The garden comes to life in the spring.",
        "Many birds migrate back home in the spring.",
        "Spring cleaning is a tradition in many households.",

        # Spring as a mechanical device
        "The spring in the mattress was poking out.",
        "He was working on a spring-loaded mechanism.",
        "The clock uses a complex arrangement of springs.",
        "When compressed, the spring releases stored energy.",
        "The toy car is powered by a wound-up spring.",
        "The spring in the pen helps it retract.",
        "She replaced the broken spring in the sofa.",
        "The trap is activated by a tension spring.",
        "Springs are essential components in mechanical watches.",
        "The engineer calculated the spring constant for the design."
    ],

    "palm": [
        # Palm of the hand
        "He wrote the reminder on the palm of his hand.",
        "The fortune teller examined the lines on her palm.",
        "She felt the warmth of the mug in her palm.",
        "He applied lotion to the rough skin of his palm.",
        "The palm of his hand was bruised after the fall.",
        "She slapped the sticker onto the palm of her hand.",
        "The palm of her hand turned red from the cold.",
        "He held the small object tightly in his palm.",
        "She traced the pattern on her palm absentmindedly.",
        "The magician concealed the coin in the palm of his hand.",

        # Palm tree
        "The beach was lined with tall palm trees.",
        "They relaxed in the shade of a palm tree.",
        "Coconuts are commonly found growing on palm trees.",
        "The palm tree swayed gently in the breeze.",
        "They decided to plant a palm tree in their yard.",
        "Date palms are known for their sweet fruits.",
        "The hurricane damaged several palm trees along the coast.",
        "Palm trees give a tropical feel to the landscape.",
        "Oil palms are cultivated for their valuable oil.",
        "The island was dotted with numerous palm trees."
    ],
       "star": [
        # Celestial body
        "The night sky was lit up with thousands of stars.",
        "Astronomers discovered a new star in the distant galaxy.",
        "The North Star has been used for navigation for centuries.",
        "Shooting stars are actually meteors entering the Earth's atmosphere.",
        "The star twinkled brightly in the dark sky.",
        "They gazed at the constellation of stars above.",
        "The death of a star can lead to a supernova.",
        "Scientists study the life cycle of stars.",
        "The telescope allowed them to see distant stars.",
        "The star's brightness varies over time.",

        # Famous person
        "She rose to fame and became a Hollywood star.",
        "The movie features several big-name stars.",
        "He dreamed of being a rock star since childhood.",
        "The young star received an award for her performance.",
        "Paparazzi followed the star everywhere she went.",
        "Fans gathered to catch a glimpse of the star.",
        "The star's autobiography became a bestseller.",
        "She was a rising star in the art world.",
        "The sports star endorsed several major brands.",
        "He was the star of the hit Broadway show."
    ],

    "turkey": [
        # Bird
        "A wild turkey crossed the road in front of them.",
        "The turkey puffed up its feathers in display.",
        "They saw a turkey roaming in the field.",
        "The farmer keeps several turkeys on his farm.",
        "Wild turkeys are native to North America.",
        "The children were delighted to see a turkey up close.",
        "Turkeys are known for their distinctive gobbling sound.",
        "The turkey hen was protecting her chicks.",
        "In autumn, turkeys become a common sight in the woods.",
        "She learned about the habitat of the turkey at school.",

        # Country
        "They planned a vacation to explore Turkey.",
        "Istanbul, Turkey, is a city rich in history.",
        "The cuisine of Turkey is known for its diverse flavors.",
        "Turkey is a transcontinental country located in Europe and Asia.",
        "The ancient ruins in Turkey attract many archaeologists.",
        "He studied the Ottoman Empire's history in Turkey.",
        "The Turkish Riviera in Turkey is a popular tourist destination.",
        "Cappadocia in Turkey is famous for its unique landscapes.",
        "The bazaars in Turkey are vibrant and full of life.",
        "Turkey's rich culture is reflected in its art and architecture."
    ],

    "jaguar": [
        # Wild cat
        "The jaguar is the largest cat in the Americas.",
        "Jaguars are known for their powerful build and beautiful spotted coats.",
        "In the rainforest, the jaguar reigns as a top predator.",
        "Jaguars prefer habitats near rivers and dense forests.",
        "Conservation efforts are crucial for the endangered jaguar.",
        "The jaguar moved stealthily through the underbrush.",
        "He was fascinated by the agility of the jaguar.",
        "Documentaries about jaguars highlight their solitary nature.",
        "The jaguar's diet mainly consists of fish, reptiles, and mammals.",
        "Jaguars have a significant role in indigenous cultures and mythologies.",

        # Luxury car
        "The new Jaguar model boasts advanced technology and sleek design.",
        "He admired the Jaguar car displayed at the showroom.",
        "Jaguar cars are known for their performance and luxury.",
        "The vintage Jaguar was the highlight of the car show.",
        "She took her Jaguar for a drive along the coast.",
        "The Jaguar's engine roared to life as he pressed the accelerator.",
        "Owning a Jaguar had been his dream for years.",
        "The Jaguar glided smoothly on the highway.",
        "He compared different Jaguar models before making a purchase.",
        "The Jaguar's interior was as impressive as its exterior."
    ],

    "bank": [

    "Children were playing on the bank of the river.",
    "The river bank was steep and covered in grass.",
    "They set up their picnic on the sunny bank.",
    "Fishermen lined the bank, casting their lines into the water.",
    "The bank was muddy after the recent rains.",
    "Wildflowers grew abundantly along the river bank.",
    "They walked along the bank looking for a spot to swim.",
    "The bank of the river provided a perfect spot for bird watching.",
    "Trees lined the bank, offering shade and shelter.",
    "The bank was eroding due to the strong current.",
    "A path wound its way down to the river bank.",
    "She sat on the bank, dipping her feet into the cool water.",

    ],

     "gorilla" : [
    "The silverback gorilla is the dominant male of the group.",
    "Gorillas share a significant amount of DNA with humans.",
    "The gorilla carefully cradled her young infant.",
    "Conservation efforts are vital for protecting gorilla habitats.",
    "Gorillas are mostly herbivorous, eating fruits, leaves, and shoots."]


}

entity_sense_discovery_data.add_data_from_dict(aug_word_sense_dict)

entity_sense_discovery_data.get_sentences_for_word('mouse')

entity_sense_discovery_data.get_sentences_for_word('apple')

entity_sense_discovery_data.get_sentences_for_word('palm')

# Save to JSON
entity_sense_discovery_data.save_to_json('entity_sense_data.json')

# Load from JSON
entity_sense_discovery_data.load_from_json('entity_sense_data.json')

# Add more data
# entity_sense_discovery_data.add_data_from_dataframe(another_df)

entity_sense_discovery_data.get_sentences_for_word('jaguar')

entity_sense_discovery_data.get_sentences_for_word('amazon')