import torch
from torch import nn
import numpy as np
from tqdm import tqdm
from . import models, data

model = models.BasicCNN()
assert torch.cuda.is_available()

device = torch.device(type="cuda")
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())

model = model.to(device)
criterion = criterion.to(device)

def train_epoch() -> tuple[int, int]:
    total_loss = 0
    total_acc = 0
    for x, y in tqdm(data.get_dataloader(4096)):
        x = x.to(device, dtype=np.float32)
        y = y.to(device)

        output = model(x)
        batch_loss = criterion(output, y)
        total_loss += batch_loss

        acc = (output.argmax(dim=1) == y).sum()
        total_acc += acc
        
        optimizer.zero_grad()
        batch_loss.backward()
        optimizer.step()

    return total_loss, total_acc

def test_epoch() -> tuple[int, int]:
    total_loss = 0
    total_acc = 0
    with torch.no_grad():
        for x, y in tqdm(data.get_dataloader(64)):
            x = x.to(device, dtype=np.float32)
            y = y.to(device)

            output = model(x)
            batch_loss = criterion(output, y)
            total_loss += batch_loss

            acc = (output.argmax(dim=1) == y).sum()
            total_acc += acc
            
            optimizer.zero_grad()
            batch_loss.backward()
            optimizer.step()
    return total_loss, total_acc

def train():
    min_loss = 10**15
    for epoch in range(100000000000000000000):
        total_loss_train, total_acc_train = train_epoch()
        total_loss_tests, total_acc_tests = test_epoch()
        print(
            f'''Epochs: {epoch+1} 
            | Train Loss: {total_loss_train / 4096:.3f}
            | Train Accuracy: {total_acc_train / 4096:.3f}
            | Test Loss: {total_loss_tests / 64:.3f}
            | Test Accuracy: {total_acc_tests / 64:.3f}'''
        )
        if min_loss > total_loss_tests / 64:
            min_loss = total_loss_tests / 64
            torch.save(model.state_dict(), "CNN.pt")
            print(f"Saved! Improved to {min_loss}")

def inference_init():
    # model.load_state_dict("CNN.pt")
    pass

def inference(image: np.array) -> str:
    return "LMAO!!"
    pass

if __name__ == '__main__':
    train()
else:
    inference_init()
