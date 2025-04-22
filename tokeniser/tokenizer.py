import csv

class PankajTokenizer:

    def __init__(self):
        try:
            self.token_map = {}
            config_path = 'tokens.csv'
            with open(config_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.token_map[row['word']] = row['token']
        except FileNotFoundError:
            print(f"Error: The file {config_path} does not exist.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def encode(self, data):
        tokens = []
        for word in list(data):
            token = self.token_map[word]
            tokens.append(token)
        return tokens

    def decode(self, tokens):
        reverse_map = {v: k for k, v in self.token_map.items()}
        data = []
        for token in tokens:
            text = reverse_map[token]
            data.append(text)
        return data