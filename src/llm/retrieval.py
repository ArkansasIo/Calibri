import torch
import torch.nn.functional as F

class InMemoryVectorStore:
    def __init__(self, dimension):
        self.dimension=dimension; self.items=[]
    def add(self,vectors,documents):
        v=F.normalize(torch.as_tensor(vectors,dtype=torch.float32),dim=-1)
        if v.size(-1)!=self.dimension: raise ValueError("embedding dimension mismatch")
        self.items.extend(zip(v,documents))
    def search(self,query,k=5):
        q=F.normalize(torch.as_tensor(query,dtype=torch.float32),dim=-1)
        scores=torch.stack([v@q for v,_ in self.items]) if self.items else torch.empty(0)
        if not len(self.items): return []
        vals,idx=torch.topk(scores,min(k,len(self.items)))
        return [(float(vals[i]),self.items[int(idx[i])][1]) for i in range(len(idx))]
