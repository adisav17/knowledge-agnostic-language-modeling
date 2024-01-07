
import pickle

class Entity_Sense_Embeddings_Data:
    def __init__(self, file_path=None):
        self.file_path = file_path
        if self.file_path:
            self.embeddings = self._load_embeddings(self.file_path)
        else:
            self.embeddings = {}

    def _load_embeddings(self, file_path):

        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def save_embeddings(self, file_path=None):

        if not file_path:
            file_path = self.file_path
        with open(file_path, 'wb') as file:
            pickle.dump(self.embeddings, file)

    def add_word_embeddings(self, word, sense_embeddings):

        self.embeddings[word] = sense_embeddings

    def get_sense_embeddings(self, word):

        return self.embeddings.get(word, None)

    def get_number_of_senses(self, word):

        if word in self.embeddings:
            return len(self.embeddings[word])
        return 0

    def update_word_embeddings(self, word, sense_embeddings):
        "
        if word in self.embeddings:
            self.embeddings[word] = sense_embeddings

    def delete_word_embeddings(self, word):

        if word in self.embeddings:
            del self.embeddings[word]



# Example usage
embeddings_data = Entity_Sense_Embeddings_Data('path_to_embeddings_file.pkl')