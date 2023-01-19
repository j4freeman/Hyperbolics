import networkx as nx
import torch
import numpy as np


def load_synthetic_data():
    tree = nx.balanced_tree(2, 7)
    adj = nx.to_numpy_matrix(tree)

    pos_mask = adj
    weight_mat = nx.floyd_warshall_numpy(tree)
    # mask = weight_mat > 0
    # weight_mat[mask] = 1 / weight_mat[mask]
    # weight_mat = np.reciprocal(weight_mat)

    neg_mask = np.zeros([len(weight_mat),len(weight_mat)])
    neg_mask[pos_mask == 0] = 1

    # print(weight_mat)

    # features = torch.ones((len(pos_mask), 4))
    # features += torch.randn_like(features) / 4

    features = np.eye(len(adj))

    weight_mat = torch.tensor(weight_mat).float()
    pos_mask = torch.tensor(pos_mask).float()
    neg_mask = torch.tensor(neg_mask).float()
    features = torch.tensor(features).float()

    print(weight_mat.shape, weight_mat.max())

    return weight_mat, pos_mask, neg_mask, features, tree