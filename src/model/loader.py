import torch
import numpy as np
from ..data.data import read_all_images

datax, datay = read_all_images()
datax = np.concatenate(datax, axis=0)
datay = np.concatenate(datay, axis=None)

class Data(torch.utils.data.Dataset):
    def __init__(self, indices):
        print(f"Getting images")
        self.x, self.y = datax[indices], datay[indices]
        print(f"Generated {len(self.x)} images from {len(self.x) // 6} captchas")

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, idx: int) -> tuple[np.array, np.int8]:
        return self.x[idx], self.y[idx]

def get_dataloader(indices):
    return torch.utils.data.DataLoader(Data(indices), batch_size=128)
