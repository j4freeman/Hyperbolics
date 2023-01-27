import torch.nn as nn
import torch
from manifolds.hyperboloid import Hyperboloid
from layers.layers import HyperbolicGraphConvolution, HypLinear

# hyperbolic feature transform
# attention aggregator
# non-linear activations varying by curvature


class HGCN(nn.Module):
    def __init__(self, nfeat, nhid, nhid2, nout, dropout, init_c=1/3, hid_c=1/2, out_c=1, use_bias=True, use_att=False, local_agg=False):
        super(HGCN, self).__init__()

        self.manifold = Hyperboloid()

        self.init_c = init_c
        self.hid_c = hid_c
        self.out_c = out_c

        self.gc1 = HyperbolicGraphConvolution(self.manifold, nfeat+1, nhid, self.init_c, self.hid_c, 0.0, act=nn.ReLU(), use_bias=use_bias, use_att=use_att, local_agg=local_agg)
        self.gc2 = HyperbolicGraphConvolution(self.manifold, nhid, nhid2, self.hid_c, self.out_c, dropout, act=nn.ReLU(), use_bias=use_bias, use_att=use_att, local_agg=local_agg)
        self.l1 = HypLinear(self.manifold, nhid2, nout, c=self.out_c, dropout=dropout, use_bias=use_bias)
        
        self.layers = nn.Sequential(self.gc1, self.gc2)

    def encode(self, x):
        o = torch.zeros_like(x)
        x = torch.cat([o[:, 0:1], x], dim=1)

        x_tan = self.manifold.proj_tan0(x, c=self.init_c)
        x_hyp = self.manifold.expmap0(x_tan, c=self.init_c)
        x_hyp = self.manifold.proj(x_hyp, c=self.init_c)
        return x_hyp

    def forward(self, x, adj):
        x_hyp = self.encode(x)

        input = (x_hyp, adj)

        out = self.layers.forward(input)
        out = self.l1.forward(out[0])
        

        return (out, adj)