import hashlib


class SimpleTokenizer:
    """Deterministic development tokenizer with stable word IDs.

    This is intentionally not a production BPE/SentencePiece tokenizer. It is
    suitable for smoke tests and reproducible tiny-model experiments.
    """
    def __init__(self, vocab_size=131072):
        if vocab_size < 8:
            raise ValueError("vocab_size must be at least 8")
        self.vocab_size = vocab_size
        self.bos_token_id = 1
        self.eos_token_id = 2
        self.unk_token_id = 3
        self._decode_cache = {}

    def _word_id(self, word):
        digest = hashlib.blake2b(word.encode("utf-8"), digest_size=8).digest()
        return (int.from_bytes(digest, "big") % (self.vocab_size - 4)) + 4

    def encode(self, text):
        ids = [self.bos_token_id]
        for word in text.split():
            token_id = self._word_id(word)
            self._decode_cache[token_id] = word
            ids.append(token_id)
        ids.append(self.eos_token_id)
        return ids

    def decode(self, ids):
        out = []
        for token_id in ids:
            if token_id in (self.bos_token_id, self.eos_token_id):
                continue
            out.append(self._decode_cache.get(int(token_id), "<unk>"))
        return " ".join(out)
