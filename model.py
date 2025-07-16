import torch
import torch.nn as nn
import torch.nn.functional as F

class model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(out_channels=5, in_channels=3, kernel_size=(2,2), stride=2) #input size is 256x256x3, output is 128x128x5
        self.conv2 = nn.Conv2d(out_channels=18, in_channels=5, kernel_size=(2,2), stride=2)#input is 64x64x5, output is 32x32x18
        self.maxPool1 = nn.MaxPool2d(kernel_size=(2,2), stride=2) #input is 128x128x5 output is 64x64x5
        self.maxPool2 = nn.MaxPool2d(kernel_size=(2,5), stride=3) #input is 32x32x18 and the output is 10x11x18
        self.linearLayer1 = nn.Linear(1980, 44)#input is 1980 dim and the output should be 44
        self.linearLayer2 = nn.Linear(44,3)#input is 44 and the output is 3
    def forward(self, x):
        #First conv and max pool then relu
        x = F.relu(self.maxPool1(self.conv1(x)))
        #second conv and maxpool then relu
        x = F.relu(self.maxPool2(self.conv2(x)))
        #flatten the output to 1980 dimension "embedding"
        highD_embed = torch.flatten(x, 1)
        #Decrease dimensions
        midD_embed = F.relu(self.linearLayer1(highD_embed))
        #Decrease to the three dimensions where the first represent bear the second represents brownies and the third is ducks
        preds = self.linearLayer2(midD_embed)
        return preds






        