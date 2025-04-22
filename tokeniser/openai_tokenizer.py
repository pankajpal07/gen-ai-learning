import tiktoken

def main():
    message = "Hello from tokeniser!"
    print(message)
    enc = tiktoken.encoding_for_model("gpt-4o")
    tokens = enc.encode(message)
    print(tokens)
    deTokens = enc.decode(tokens)
    print(deTokens)

if __name__ == "__main__":
    main()
