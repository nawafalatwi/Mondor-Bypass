import torch
from torch import nn
import numpy as np
from tqdm import tqdm
from . import models
from ..data import data

model = models.BasicCNN()
assert torch.cuda.is_available()

device = torch.device(type="cuda")
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())

model.load_state_dict(torch.load("CNN.pt"))
model = model.to(device)
criterion = criterion.to(device)

def inference(image: bytes):
    result = []
    for img, _ in data.split_image(image, "AAAAAA"):
        img = torch.tensor(img).to(device, dtype=torch.float)
        print(img.shape)
        idx = model(img).argmax(dim=1)
        result.append(data.decode_result(idx))
    return str(result)
