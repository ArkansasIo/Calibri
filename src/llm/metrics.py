import math
def token_accuracy(logits,labels,ignore_index=-100):
    pred=logits[:,:-1].argmax(-1); target=labels[:,1:]
    mask=target.ne(ignore_index)
    return float((pred[mask]==target[mask]).float().mean()) if mask.any() else 0.0
def bits_per_token(loss): return float(loss)/math.log(2)
