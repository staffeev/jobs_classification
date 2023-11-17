import torch
from navec import Navec
from slovnet.model.emb import NavecEmbedding

path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'  # 51MB
navec = Navec.load(path)  # ~1 sec, ~100MB RAM

words = ['блять', "блядь"]
ids = [navec.vocab[e] for e in words]
resume1 = ""
emb = NavecEmbedding(navec)
input = torch.tensor(ids)

print(emb(input))  # 3 x 300