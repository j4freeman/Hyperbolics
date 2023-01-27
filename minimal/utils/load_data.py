import networkx as nx
import torch
import numpy as np


def load_synthetic_data(depth=7):
    tree = nx.balanced_tree(2, depth)
    adj = nx.to_numpy_matrix(tree)

    features = np.eye(len(adj))

    adj = torch.tensor(adj).float()
    features = torch.tensor(features).float()

    return adj, features, tree