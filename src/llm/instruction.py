"""Instruction/chat formatting and supervised fine-tuning utilities."""
def format_messages(messages,system_prompt=None):
    rows=[]
    if system_prompt: rows.append(("system",system_prompt))
    for m in messages:
        role=m["role"]; content=m["content"]
        if role not in {"system","user","assistant","tool"}: raise ValueError("invalid role")
        rows.append((role,content))
    return "\n".join(f"<|{r}|>\n{c}" for r,c in rows)

def sft_loss(logits,labels,mask=None):
    import torch.nn.functional as F
    target=labels[:,1:]
    pred=logits[:,:-1]
    loss=F.cross_entropy(pred.reshape(-1,pred.size(-1)),target.reshape(-1),ignore_index=-100,reduction="none")
    if mask is not None: loss=loss*mask[:,1:].reshape(-1)
    return loss.mean()
