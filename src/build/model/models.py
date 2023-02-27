import torch
from torch import nn

device: torch.device

if torch.cuda.is_available():
    print("CUDA is available!")
    device = torch.device(type="cuda")
else:
    print("CUDA is not available!")
    device = torch.device(type="cpu")

# Model that receives 32x32 images
class BasicCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # 16x32x1 -> 8x16x16
        self.convo1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=1)
        )

        # 8x16x16 -> 4x8x64
        self.convo2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=64, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=1)
        )

        # 4x8x64 -> 2x4x64
        self.average = nn.AvgPool2d(kernel_size=2, stride=2)
        
        # 2x4x64
        self.classifier = nn.Sequential(
            nn.Linear(2*4*64, 100),
            nn.ReLU(),
            nn.Linear(100, 36)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.convo1(x)
        x = self.convo2(x)
        x = self.average(x)

        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
