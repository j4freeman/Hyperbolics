import time
import numpy as np
import os
import torch
import torch.optim as optim
import networkx as nx
from models.hgcn import HGCN
import matplotlib.pyplot as plt

from manifolds.hyperboloid import Hyperboloid

from utils.load_virginia import load_synthetic_data

import shutil

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
weight_mat, pos_mask, neg_mask, features, G = load_synthetic_data()

paths = nx.shortest_path_length(G,0)

colors = [x[1] for x in paths.items()]

adj = []

for idx1, row in enumerate(pos_mask):
    for idx2, v in enumerate(row):
      if v == 1 and idx2 >= idx1:
        adj.append((idx1, idx2))



# init_c = nn.Parameter(torch.Tensor([1.]))
# init_c = 0.25
# hid_c = nn.Parameter(torch.Tensor([0.6]))
# out_c = nn.Parameter(torch.Tensor([0.5]))

init_c = 1.
hid_c = 0.6
out_c = 0.2

# Model and optimizer
model = HGCN(nfeat=features.shape[1],
            nhid=32,
            nhid2=64,
            nhid3=-1,
            nout=3,
            dropout=0.1,
            init_c=init_c,
            hid_c=hid_c,
            out_c=out_c)

EPS = 1e-15

model = model.to(device)
# hyperbolic_model = model.to(device)
weight_mat = weight_mat.to(device)
pos_mask = pos_mask.to(device)
neg_mask = neg_mask.to(device)
features = features.to(device)

N_pos = pos_mask.sum()
N_neg = neg_mask.sum()

dists = []

# Train model
t_total = time.time()
loss_list = []
neg_losses = []
pos_losses = []
outputs = []
fermis = []

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

epochs = 1500

optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)

for epoch in range(epochs):

    t = time.time()
    model.train()
    optimizer.zero_grad()
    output, k = model(features, pos_mask) 
    # print(features.shape, output.shape)
    # output = output[:, 1:]

    x_1 = output.repeat(output.size(0),1)
    x_2 = output.repeat_interleave(output.size(0),0)

    dist_mat = Hyperboloid().sqdist(x_1, x_2, c=out_c).view(output.size(0),output.size(0))

    simi = dist_mat ** 0.5

    pos_sim = simi * pos_mask
    neg_sim = simi * neg_mask
    h = simi * (weight_mat - pos_mask)

    l1_loss = 0.
    l2_loss = 0.

    for p in model.parameters():
        l1_loss += torch.linalg.norm(p,1)
        l2_loss += torch.linalg.norm(p,2)


    neg_sum = neg_sim.sum(dim=1).unsqueeze(1).repeat(1,output.size(0))
    loss = torch.div(pos_sim, neg_sum).sum()

    # loss = pos_sim.sum() / neg_sim.sum()

    # loss /= h.sum()

    fermi_dirac = (1. + torch.exp(dist_mat)) ** -1.

    loss = torch.nn.BCELoss()(fermi_dirac, pos_mask)

    embeds_poincare = Hyperboloid().to_poincare(output, c=model.out_c).cpu().detach()

    # loss += torch.norm(embeds_poincare) / 10

    if epoch == 0:
      init_pos = pos_sim.sum().item()
      init_neg = neg_sim.sum().item()
      init_loss = loss.item()
      init_h = h.sum().item()

    loss_list.append(loss.item())

    loss.backward()
    optimizer.step()


    # print("Poincare shape: ", embeds_poincare.size())
    # print(embeddings[:15])
    # print(" -> Poincare")
    # print(embeds_poincare[:15])

    if epoch%25 == 0 or epoch == epochs - 1:
      model.eval()
      output, k = model(features, pos_mask) 
      plt.gca().add_patch(plt.Circle((0, 0), 1/model.out_c.item(), color='black', fill=False))
      plt.title("Epoch: " + str(epoch))
      
      embeds_poincare = Hyperboloid().to_poincare(output, c=model.out_c).cpu().detach()

      plt.scatter(embeds_poincare[:,0], embeds_poincare[:,1], s=25, alpha=0.8, c=colors, cmap="viridis_r", edgecolors='black')

      for pair in adj:
        plt.plot([embeds_poincare[pair[0]][0], embeds_poincare[pair[1]][0]], [embeds_poincare[pair[0]][1], embeds_poincare[pair[1]][1]], '-', 
        color="gray", alpha=0.5,linewidth=0.5)
    
      ax.set_aspect('equal')
      plt.axis('off')
      plt.savefig("img/" + str(epoch) + '.png')
      plt.cla()

      print('Epoch: {:04d}'.format(epoch),
          'Loss_Avg: {:.5f}'.format(sum(loss_list[-25:]) / 25),
          'Time: {:.4f}s'.format(time.time() - t),
          'C1: {:.2f}'.format(model.init_c.item()),
          'C2: {:.2f}'.format(model.c2.item()),
          'C3: {:.2f}'.format(model.out_c.item()),
          'Grd: {:.2f}'.format(sum([param.grad.abs().sum() if param.grad is not None else 0 for _, param in model.named_parameters()])),
          )

print("Optimization Finished!")
print("Total time elapsed: {:.4f}s".format(time.time() - t_total))
print((fermi_dirac - pos_mask).abs().sum().item())