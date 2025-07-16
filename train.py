import torch
import torch.optim as optim
import torch.utils.data as data
import torch.nn as nn
import torchvision.datasets as ds
from torchvision.transforms import v2
from torch.optim.lr_scheduler import StepLR
import Model

if __name__ == "__main__":
    optimizer = optim.Adam(Model.model.parameters(), lr=0.001)
    scheduler = StepLR(optimizer, step_size=10, gamma=0.1)
    lossFunction = nn.CrossEntropyLoss()

    transforms = v2.Compose([
        v2.ToImage(),
        v2.RandomResizedCrop(size=(256,256), antialias=True),
        v2.RandomHorizontalFlip(p=0.5),
        v2.ToDtype(torch.float32, scale=True),
        v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    trainImages = ds.ImageFolder(root="./train", transform=transforms)
    trainLoader = torch.utils.data.DataLoader(trainImages, batch_size=4, shuffle=True, num_workers=2)

    validationImages = ds.ImageFolder(root="./validation", transform=transforms)
    validationLoader = torch.utils.data.DataLoader(validationImages, batch_size=2, num_workers=2)


    for epoch in range(5):
        Model.model.train()
        runningLoss = 0
        otherLoss = 0
        for i, data in enumerate(trainLoader):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = Model.model(inputs)
            loss=lossFunction(outputs, labels)
            loss.backward()
            optimizer.step()
            runningLoss +=loss.item()
        scheduler.step()

        otherLoss = 0.0
        total = 0
        correct = 0
        Model.model.eval()
        with torch.no_grad(): 
            for i, data, in enumerate(validationLoader):
                inputs, labels = data
                outputs = Model.model(inputs)
                predictions = torch.argmax(outputs, dim=1)
                total+= len(inputs)
                for i in range(len(predictions)):
                    if predictions[i] == labels[i]:
                        correct+=1
                    
                loss=lossFunction(outputs, labels)
                otherLoss +=loss.item()


        print(f"Epoch {epoch}: Trainset Loss {runningLoss/(len(trainLoader))}")
        print(f"Epoch {epoch}: Validation Set Loss {otherLoss/len(validationLoader)}")
        print(f"Epoch {epoch}: Validation Set Accurcy {correct/total}")
        




