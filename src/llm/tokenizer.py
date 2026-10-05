class SimpleTokenizer:
    """Small deterministic tokenizer for development and smoke tests.

    Replace with a trained BPE/SentencePiece tokenizer for production training.
    """
    def __init__(self, vocab_size=131072):
        self.vocab_size = vocab_size
        self.bos_token_id = 1
        self.eos_token_id = 2

    def encode(self, text):
        ids = [self.bos_token_id]
        ids.extend((hash(word) % (self.vocab_size - 3)) + 3 for word in text.split())
        ids.append(self.eos_token_id)
        return ids

    def decode(self, ids):
        return " ".join(str(i) for i in ids)
