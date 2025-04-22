from tokenizer import PankajTokenizer

tokenizer = PankajTokenizer()
english = 'The quick brown fox jumps over a lazy dog'
tokens = tokenizer.encode(english)
print("Tokens: ", tokens)
data = tokenizer.decode(tokens)
print("Data: ", ''.join(data))