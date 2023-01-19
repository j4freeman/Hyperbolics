import time
import numpy as np
import os
import torch
import torch.optim as optim
import networkx as nx
import torch.nn as nn
from models.hgcn import HGCN
import matplotlib.pyplot as plt

from manifolds.hyperboloid import Hyperboloid

from utils.load_data import load_synthetic_data

import shutil

if os.path.exists('./img'):
  shutil.rmtree('./img')
os.mkdir("./img")


seed = 0
np.random.seed(seed)
torch.manual_seed(seed)

torch.cuda.get_device_name(0)

GPU = True
device_idx = 1
if GPU:
    device = torch.device("cuda:" + str(device_idx - 1) if torch.cuda.is_available() else "cpu")
    torch.cuda.manual_seed(seed)
else:
    device = torch.device("cpu")
    torch.set_num_threads(16)

print("CUDA Status is: ", device)

# Load data
adj, features, G = load_synthetic_data()

paths = nx.shortest_path_length(G,0)

colors = [x[1] for x in paths.items()]

init_c = nn.Parameter(torch.Tensor([1.0]), requires_grad=False)
hid_c = nn.Parameter(torch.Tensor([0.5]), requires_grad=False)
out_c = nn.Parameter(torch.Tensor([0.25]), requires_grad=False)

# Model and optimizer
model = HGCN(nfeat=features.shape[1],
            nhid=32,
            nhid2=64,
            nout=3,
            dropout=0.1,
            init_c=init_c,
            hid_c=hid_c,
            out_c=out_c)

model = model.to(device)
# hyperbolic_model = model.to(device)
adj = adj.to(device)
features = features.to(device)

adj_list = []

for idx1, row in enumerate(adj):
    for idx2, v in enumerate(row):
      if v == 1 and idx2 >= idx1:
        adj_list.append((idx1, idx2))


# Train model
t_total = time.time()
loss_list = []

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

epochs = 500

optimizer = optim.Adam(model.parameters(), lr=5e-3, weight_decay=1e-5)

for epoch in range(epochs):

    t = time.time()
    model.train()
    optimizer.zero_grad()
    output, k = model(features, adj) 

    x_1 = output.repeat(output.size(0),1)
    x_2 = output.repeat_interleave(output.size(0),0)

    dist_mat = Hyperboloid().sqdist(x_1, x_2, c=out_c).view(output.size(0),output.size(0))

    fermi_dirac = (1. + torch.exp(dist_mat)) ** -1.

    loss = torch.nn.BCELoss()(fermi_dirac, adj)

    loss_list.append(loss.item())

    loss.backward()
    optimizer.step()

    if epoch%25 == 0 or epoch == epochs - 1:
      model.eval()
      output, k = model(features, adj) 
      plt.gca().add_patch(plt.Circle((0, 0), 1/model.out_c.item(), color='black', fill=False))
      plt.title("Epoch: " + str(epoch))
      
      embeds_poincare = Hyperboloid().to_poincare(output, c=model.out_c).cpu().detach()

      plt.scatter(embeds_poincare[:,0], embeds_poincare[:,1], s=25, alpha=0.8, c=colors, cmap="viridis_r", edgecolors='black')

      for pair in adj_list:
        plt.plot([embeds_poincare[pair[0]][0], embeds_poincare[pair[1]][0]], [embeds_poincare[pair[0]][1], embeds_poincare[pair[1]][1]], '-', 
        color="gray", alpha=0.5,linewidth=0.5)
    
      ax.set_aspect('equal')
      plt.axis('off')
      plt.savefig("img/" + str(epoch) + '.png')
      plt.cla()

      if epoch < 25:
        continue
      print('Epoch: {:04d}'.format(epoch),
          'Loss_Avg: {:.5f}'.format(sum(loss_list[-25:]) / 25),
          'Time: {:.4f}s'.format(time.time() - t),
          'C1: {:.2f}'.format(model.init_c.item()),
          'C2: {:.2f}'.format(model.hid_c.item()),
          'C3: {:.2f}'.format(model.out_c.item()),
          'Grd: {:.2f}'.format(sum([param.grad.abs().sum() if param.grad is not None else 0 for _, param in model.named_parameters()])),
          )

print("Optimization Finished!")
print("Total time elapsed: {:.4f}s".format(time.time() - t_total))
print((fermi_dirac - adj).abs().sum().item())