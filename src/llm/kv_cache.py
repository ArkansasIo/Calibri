import torch


class KVCache:
    """Simple validated per-layer KV cache container for autoregressive inference."""
    def __init__(self, num_layers):
        if num_layers < 1:
            raise ValueError("num_layers must be positive")
        self.keys = [None] * num_layers
        self.values = [None] * num_layers

    def clear(self):
        self.keys = [None] * len(self.keys)
        self.values = [None] * len(self.values)

    def append(self, layer, key, value):
        if not 0 <= layer < len(self.keys):
            raise IndexError(layer)
        if key.ndim != 4 or value.ndim != 4:
            raise ValueError("cached keys and values must be rank-4 tensors")
        if key.shape != value.shape:
            raise ValueError("key/value cache shapes must match")
        if self.keys[layer] is None:
            self.keys[layer], self.values[layer] = key, value
        else:
            self.keys[layer] = torch.cat((self.keys[layer], key), dim=-2)
            self.values[layer] = torch.cat((self.values[layer], value), dim=-2)
        return self.keys[layer], self.values[layer]

    def get(self, layer):
        if not 0 <= layer < len(self.keys):
            raise IndexError(layer)
        if self.keys[layer] is None:
            return None
        return self.keys[layer], self.values[layer]
