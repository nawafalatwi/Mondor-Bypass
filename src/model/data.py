import torch
import numpy as np

def generate_single_image() -> tuple[np.array, np.int8]:
    pass

class Data(torch.utils.data.Dataset):
    def __init__(self, size: int):
        self.size = size

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, idx: int) -> tuple[np.array, np.int8]:
        return generate_single_image()

def get_dataloader(size: int):
    return torch.utils.data.DataLoader(Data(size), batch_size=32)
