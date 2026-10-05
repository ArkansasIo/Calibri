import torch

class LLMService:
    def __init__(self,model,tokenizer,device=None):
        self.device=device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model=model.to(self.device).eval(); self.tokenizer=tokenizer
    @torch.no_grad()
    def generate_text(self,prompt,generate_fn,**kwargs):
        ids=torch.tensor([self.tokenizer.encode(prompt)],device=self.device)
        out=generate_fn(self.model,ids,**kwargs)
        return self.tokenizer.decode(out[0].tolist())
