class KVCache:
    """Simple per-layer KV cache container for autoregressive inference."""
    def __init__(self, num_layers):
        self.keys = [None] * num_layers
        self.values = [None] * num_layers

    def clear(self):
        self.keys = [None] * len(self.keys)
        self.values = [None] * len(self.values)

    def append(self, layer, key, value):
        self.keys[layer] = key if self.keys[layer] is None else self.keys[layer].__class__.cat((self.keys[layer], key), dim=-2)
        self.values[layer] = value if self.values[layer] is None else self.values[layer].__class__.cat((self.values[layer], value), dim=-2)
        return self.keys[layer], self.values[layer]
