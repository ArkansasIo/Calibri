import unittest
import torch

from src.llm import AetherForgeLLM, ModelConfig, SimpleTokenizer, GenerateConfig, generate
from src.llm.losses import causal_lm_loss, label_smoothed_loss
from src.llm.safety import SafetyPolicy, validate_generation
from src.llm.kv_cache import KVCache
from src.integrations.engine_bridge import detect_engine
from src.integrations.language_registry import detect_language


class CoreTests(unittest.TestCase):
    def test_tokenizer_is_stable(self):
        tok = SimpleTokenizer(128)
        a = tok.encode("hello world")
        b = tok.encode("hello world")
        self.assertEqual(a, b)
        self.assertEqual(tok.decode(a), "hello world")

    def test_empty_loss_is_finite(self):
        logits = torch.randn(1, 3, 16)
        labels = torch.full((1, 3), -100)
        self.assertEqual(float(causal_lm_loss(logits, labels)), 0.0)
        self.assertEqual(float(label_smoothed_loss(logits, labels, 0.1)), 0.0)

    def test_model_forward_and_generation(self):
        torch.manual_seed(1)
        model = AetherForgeLLM(ModelConfig(vocab_size=32, hidden_size=8, num_layers=2,
                                           num_attention_heads=2, num_key_value_heads=1,
                                           intermediate_size=16))
        ids = torch.tensor([[1, 4, 5]])
        out = model(ids, labels=ids, use_cache=True)
        self.assertEqual(tuple(out["logits"].shape), (1, 3, 32))
        generated = generate(model, ids, GenerateConfig(max_new_tokens=3, do_sample=False, use_cache=True))
        self.assertEqual(generated.shape[1], 6)

    def test_kv_cache(self):
        cache = KVCache(1)
        k = torch.zeros(1, 1, 1, 2)
        v = torch.ones_like(k)
        cache.append(0, k, v)
        cache.append(0, k, v)
        self.assertEqual(cache.get(0)[0].shape[-2], 2)

    def test_safety(self):
        validate_generation({"input_ids": [1, 2], "max_new_tokens": 4})
        with self.assertRaises(PermissionError):
            validate_generation({"input_ids": [1], "max_new_tokens": 4, "tool_call": True})

    def test_detection(self):
        self.assertEqual(detect_language("main.cpp"), "C++")
        self.assertEqual(detect_engine("." ).engine, "custom")


if __name__ == "__main__":
    unittest.main()
