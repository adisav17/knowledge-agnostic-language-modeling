import os
os.chdir('/content/drive/My Drive/kalm/kalm_lm/entity_sense_discovery')

import pandas as pd
import ast
import json
from collections import defaultdict
import pickle

import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from entity_sense_discovery_data import Entity_Sense_Discovery_Data
import warnings



# cuda preferred for compute (A100/V100)

if torch.cuda.is_available():   
    device = 'cuda'
else:
    device = 'cpu'


"""
class EntitySenseDiscoveryKMeans core functionality:
find the optimal value of the number of distinct entity senses for a word in coprus, 
find clusters of sentences for in view of entity sense usaage, 
find entity sense embeddings for every distinct entity sense for a given entity word 
"""

class EntitySenseDiscoveryKMeans:
    def __init__(self, word_sense_document, tokenizer, model, device):
        self.word_sense_document = word_sense_document
        self.tokenizer = tokenizer
        self.model = model.to(device) ## gpu adjust here

    def get_embeddings_for_sentences_of_word(self, word):
        """Generate BERT embeddings for sentences containing a specific word."""
        sentences = self.word_sense_document.get(word, [])
        embeddings = []
        for sentence in sentences:
            inputs = self.tokenizer(sentence, return_tensors='pt', truncation=True, max_length=512).to(device) ## gpu adjust here
            outputs = self.model(**inputs)
            sentence_embedding = outputs.last_hidden_state.mean(dim=1)
            embeddings.append(sentence_embedding.detach().cpu().numpy()[0]) ## gpu adjust here
        return embeddings

    def find_clusters_for_sentences_of_word(self, embeddings, num_clusters=2):
        """Cluster sentences using K-means and return cluster labels."""
        embeddings_array = np.array(embeddings)
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(embeddings_array)
        return kmeans.labels_

    def get_word_embeddings_from_sentences(self, word, sentences):
        """Extract contextualized embeddings for a specific word from each sentence."""
        word_embeddings = []

        for sentence in sentences:
            # Tokenize the sentence and convert to tensor
            inputs = self.tokenizer(sentence, return_tensors='pt', truncation=True, max_length=512).to(device) ## gpu adjust here
            outputs = self.model(**inputs, output_hidden_states = True)

            # Identify the token indices corresponding to the word
            tokenized_sentence = self.tokenizer.tokenize(sentence)
            word_token_indices = [i for i, token in enumerate(tokenized_sentence) if word in token]

            # Extract the embeddings for the word
            if word_token_indices:
                # Find the corresponding layers' embeddings
                all_layers = outputs.hidden_states
                word_layers = [all_layers[layer][0, index] for layer in range(len(all_layers)) for index in word_token_indices]
                # Average over all layers and word occurrences to get a single vector
                word_embedding = torch.mean(torch.stack(word_layers), dim=0)
                word_embeddings.append(word_embedding.detach().cpu().numpy()) ## gpu adjust here

        return word_embeddings



    def get_sense_embeddings_for_word_from_clusters(self, word, cluster_labels):
        """Get average embeddings of the word itself, partitioned by cluster."""
        sentences = self.word_sense_document.get(word, [])
        word_embeddings = self.get_word_embeddings_from_sentences(word, sentences)

        unique_labels = set(cluster_labels)
        sense_embeddings = {}
        for label in unique_labels:
            cluster_word_embeds = np.array(word_embeddings)[np.array(cluster_labels) == label]
            if cluster_word_embeds.size > 0:
                sense_embeddings[label] = np.mean(cluster_word_embeds, axis=0)
        return sense_embeddings


    def get_sentences_per_cluster_for_word(self, word, num_clusters = 2):

       sentences_for_word = self.word_sense_document.get(word, [])
       sentence_embeddings = self.get_embeddings_for_sentences_of_word(word)
       cluster_labels = self.find_clusters_for_sentences_of_word(sentence_embeddings, num_clusters)

       sentences_per_cluster = {}
       for label, sentence in zip(cluster_labels, sentences_for_word):
           if label not in sentences_per_cluster:
                sentences_per_cluster[label] = []
           sentences_per_cluster[label].append(sentence)
       return sentences_per_cluster


    def discover_sense_embeddings_for_given_clusters(self, word, num_clusters=2):
        """Generate sense embeddings for a given word."""
        sentence_embeddings = self.get_embeddings_for_sentences_of_word(word)
        cluster_labels = self.find_clusters_for_sentences_of_word(sentence_embeddings, num_clusters)
        entity_sense_embeddings = self.get_sense_embeddings_for_word_from_clusters(word, cluster_labels)
        return entity_sense_embeddings

    def calculate_wcss(self, word, num_clusters):
        """Calculate the total within-cluster sum of square (WCSS)."""
        sentence_embeddings = self.get_embeddings_for_sentences_of_word(word)
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(sentence_embeddings)
        wcss = kmeans.inertia_
        return wcss

    def find_silhouette_score(self,word, num_clusters):

      sentence_embeddings = self.get_embeddings_for_sentences_of_word(word)
      embeddings_array = np.array(sentence_embeddings)
      kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(embeddings_array)
      labels = kmeans.labels_
      silhouette_avg = silhouette_score(embeddings_array, labels)

      return silhouette_avg


    def find_optimal_clusters_for_word(self, word, max_clusters=5):
        """Determine the optimal number of clusters for a given word using silhouette analysis."""
        sentence_embeddings = self.get_embeddings_for_sentences_of_word(word)
        embeddings_array = np.array(sentence_embeddings)

        best_score = -1
        optimal_clusters = 2

        for n_clusters in range(2, max_clusters):
            kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(embeddings_array)
            labels = kmeans.labels_
            silhouette_avg = silhouette_score(embeddings_array, labels)

            if silhouette_avg > best_score:
                best_score = silhouette_avg
                optimal_clusters = n_clusters

        return optimal_clusters

    def find_optimal_clusters_sense_embeddings_for_word(self, word, max_clusters=5):

        optimal_entity_sense_embeddings = {}
        sentence_embeddings = self.get_embeddings_for_sentences_of_word(word)
        embeddings_array = np.array(sentence_embeddings)

        kmeans_1 = KMeans(n_clusters= 1, random_state=0).fit(embeddings_array)
        labels_1 = kmeans_1.labels_
        entity_sense_embeddings_1 = self.get_sense_embeddings_for_word_from_clusters(word, labels_1)

        best_score = -1
        optimal_clusters = 2

        for n_clusters in range(2, max_clusters):
            kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(embeddings_array)
            labels = kmeans.labels_
            silhouette_avg = silhouette_score(embeddings_array, labels)
            entity_sense_embeddings = self.get_sense_embeddings_for_word_from_clusters(word, labels)

            if silhouette_avg > best_score:
                best_score = silhouette_avg
                optimal_clusters = n_clusters
                optimal_entity_sense_embeddings = entity_sense_embeddings

        if(best_score < 0.105):
          # see empirical threshold estimation
          optimal_entity_sense_embeddings = entity_sense_embeddings_1


        return optimal_entity_sense_embeddings



## useful functions, for evalutation, hyperparameter tuning 


def display_silhouette_scores(word_list, cluster_list):

  for word in word_list:
    print(word)
    for cluster in cluster_list:
      print(esd_kmeans.find_silhouette_score(word,cluster))
    print(" ")

def print_cluster_sentences(cluster_sense_dictionary):

  for cluster,sentences in cluster_sense_dictionary.items():

    print(f"Cluster {cluster}:")
    print(" ")
    for sent in sentences:
        print(f" - {sent}")
    print(" ")

def display_wcss_scores(word_list, cluster_list):

  for word in word_list:
    print(word)
    for cluster in cluster_list:
      print(esd_kmeans.calculate_wcss(word,cluster)/len(word_sense_document[word]))
    print(" ")

def find_max_silhouette_for_word(word_list, cluster_list):

  max_score_for_words = {}
  max_cluster_for_words = {}

  for word in word_list:

    max_score = 0
    max_cluster = 0
    for cluster in cluster_list:
      score = esd_kmeans.find_silhouette_score(word,cluster)
      if score > max_score:
        max_score = score
        max_cluster = cluster

    print(word)
    print(max_score)
    print(" ")
    max_score_for_words[word] = max_score
    max_cluster_for_words[word] = max_cluster

  return max_score_for_words, max_cluster_for_words


def find_wcss_difference_for_word(word_list):

  wcss_difference_for_words = {}

  for word in word_list:


    wcss_1 = (esd_kmeans.calculate_wcss(word,1))/len(word_sense_document[word])
    wcss_2 = (esd_kmeans.calculate_wcss(word,2))/len(word_sense_document[word])

    wcss_difference = 0

    if wcss_1 > wcss_2:
      wcss_difference = wcss_1 - wcss_2

    print(word)
    print(wcss_difference)
    wcss_difference_for_words[word] = wcss_difference




## usage, sentence clusters and entity sense embedding development and testing


entity_sense_discovery_data =  Entity_Sense_Discovery_Data()
entity_sense_discovery_data.load_from_json('entity_sense_data.json')

word_sense_document = entity_sense_discovery_data.entity_sentences.copy()

word_sense_document['mouse']


warnings.simplefilter(action='ignore', category=FutureWarning)

model_name='bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

esd_kmeans = EntitySenseDiscoveryKMeans(word_sense_document, tokenizer, model, device )


# testing 

word = 'jaguar'

esd_kmeans.get_sentences_per_cluster_for_word(word, 2)

esd_kmeans.find_optimal_clusters_sense_embeddings_for_word('jaguar', max_clusters=4).keys()

esd_kmeans.find_optimal_clusters_sense_embeddings_for_word('apple', max_clusters=4).keys()

esd_kmeans.find_optimal_clusters_sense_embeddings_for_word('gorilla', max_clusters=4).keys()

esd_kmeans.find_optimal_clusters_sense_embeddings_for_word('india', max_clusters=4).keys()

esd_kmeans.find_optimal_clusters_sense_embeddings_for_word('amazon', max_clusters=4).keys()

esd_kmeans.find_optimal_clusters_for_word('jaguar',4)

esd_kmeans.discover_sense_embeddings_for_given_clusters(word, 2)[0].shape

esd_kmeans.find_optimal_clusters_for_word(word,4)

# potential single senses
single_sense_word_list = ['gorilla','india','china', 'everest', 'army', 'japan', 'fifteen','england','shakespeare']
# potential multiple senses
multiple_sense_word_list = [ 'jaguar', 'mouse', 'apple', 'turkey', 'amazon', 'palm', 'star','bank','mercury' ]
cluster_list = [2,3,4]





## testing     

esd_kmeans.find_silhouette_score('japan', 2)

find_max_silhouette_for_word(['mercury'], cluster_list)

max_score_for_words, max_cluster_for_words = find_max_silhouette_for_word(single_sense_word_list, cluster_list)

max_score_for_words_2, max_cluster_for_words_2 = find_max_silhouette_for_word(multiple_sense_word_list, cluster_list)

max_cluster_for_words_2['orange']

max_score_for_words_2['orange']

esd_kmeans.find_optimal_clusters_for_word('orange',5)

esd_kmeans.find_silhouette_score('orange', 4)

esd_kmeans.find_silhouette_score('orange', 3)

esd_kmeans.find_silhouette_score('orange', 2)

max_cluster_for_words['army']

max_cluster_for_words_2['mercury']

max_cluster_for_words['shakespeare']

print_cluster_sentences(esd_kmeans.get_sentences_per_cluster_for_word('shakespeare', 2))

print_cluster_sentences(esd_kmeans.get_sentences_per_cluster_for_word('mouse', 3))

print_cluster_sentences(esd_kmeans.get_sentences_per_cluster_for_word('army', 2))

print_cluster_sentences(esd_kmeans.get_sentences_per_cluster_for_word('army', 3))

word_sense_document['river']

esd_kmeans.find_optimal_clusters_for_word('river',5)

find_max_silhouette_for_word(['river'], cluster_list)

print_cluster_sentences(esd_kmeans.get_sentences_per_cluster_for_word('river', 3))

find_max_silhouette_for_word(['river'], cluster_list)

print_cluster_sentences(esd_kmeans.get_sentences_per_cluster_for_word('mercury', 2))

print_cluster_sentences(esd_kmeans.get_sentences_per_cluster_for_word('orange', 4))

wcss_diff_words = find_wcss_difference_for_word(single_sense_word_list)

wcss_diff_words = find_wcss_difference_for_word(multiple_sense_word_list)



combined_list  = single_sense_word_list +  multiple_sense_word_list


word_sense_dict = {}
for word in combined_list:
  print(word)
  word_sense_dict[word] = esd_kmeans.find_optimal_clusters_sense_embeddings_for_word(word, max_clusters=4)

word_sense_dict['jaguar'].keys()

word_sense_dict['turkey'].keys()

word_sense_dict['india'].keys()

word_sense_dict['china'].keys()

word_sense_dict['gorilla']

word_sense_dict['gorilla'][0].shape

# save entity sense embeddings 

def save_with_pickle(data, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

save_with_pickle(word_sense_dict, 'generated_entity_sense_embeddings.pkl')

def load_with_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

word_sense_dict_new = load_with_pickle('generated_entity_sense_embeddings.pkl')


# testing 
assert (word_sense_dict_new['gorilla'][0] == word_sense_dict['gorilla'][0])