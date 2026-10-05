"""Reference tensor-parallel linear layers using torch.distributed collectives."""
import torch
import torch.nn as nn
import torch.distributed as dist

class ColumnParallelLinear(nn.Module):
    def __init__(self,in_features,out_features,bias=True):
        super().__init__()
        if dist.is_initialized(): world=dist.get_world_size()
        else: world=1
        if out_features%world: raise ValueError("out_features must divide world size")
        self.world=world; self.local_out=out_features//world
        self.weight=nn.Parameter(torch.empty(self.local_out,in_features))
        self.bias=nn.Parameter(torch.zeros(self.local_out)) if bias else None
        nn.init.normal_(self.weight,std=in_features**-0.5)
    def forward(self,x):
        return torch.nn.functional.linear(x,self.weight,self.bias)

class RowParallelLinear(nn.Module):
    def __init__(self,in_features,out_features,bias=True):
        super().__init__()
        world=dist.get_world_size() if dist.is_initialized() else 1
        if in_features%world: raise ValueError("in_features must divide world size")
        self.world=world; self.local_in=in_features//world
        self.weight=nn.Parameter(torch.empty(out_features,self.local_in))
        self.bias=nn.Parameter(torch.zeros(out_features)) if bias else None
        nn.init.normal_(self.weight,std=self.local_in**-0.5)
    def forward(self,x):
        y=torch.nn.functional.linear(x,self.weight,self.bias)
        if self.world>1:
            dist.all_reduce(y)
        return y
