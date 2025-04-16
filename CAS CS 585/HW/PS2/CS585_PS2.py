from __future__ import print_function
from PIL import Image
import os
import os.path
import numpy as np
import sys
if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle

import torch.utils.data as data
from torchvision.datasets.utils import download_url, check_integrity
import copy
import csv
import matplotlib
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import os.path
from tqdm.notebook import tqdm
import sys
import torch
import torch.utils.data
import torchvision
import torchvision.transforms as transforms

from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

np.random.seed(111)
torch.cuda.manual_seed_all(111)
torch.manual_seed(111)


class CIFAR10Test(torchvision.datasets.VisionDataset):
    def __init__(self, root, transform=None ):
        super(CIFAR10Test, self).__init__(root, transform=transform)

        image_filename = os.path.join(root, 'cifar10_test_images.npy') # where is this file coming from?
        images = np.load(image_filename)

        assert len(images.shape) == 4
        assert images.shape[0] == 2000
        assert images.shape[1] == 32
        assert images.shape[2] == 32
        assert images.shape[3] == 3

        self.data = images

    def __getitem__(self, index):
        img = self.data[index]

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = Image.fromarray(img)

        if self.transform is not None:
            img = self.transform(img) # where is this variable?

        return img

    def __len__(self):
        return len(self.data) # Maybe 2000?


def calculate_accuracy(dataloader, model, is_gpu):
    """ Util function to calculate val set accuracy,
    both overall and per class accuracy
    Args:
        dataloader (torch.utils.data.DataLoader): val set
        is_gpu (bool): whether to run on GPU
    Returns:
        tuple: (overall accuracy, class level accuracy)
    """
    correct = 0.
    total = 0.
    predictions = []

    class_correct = list(0. for i in range(TOTAL_CLASSES))
    class_total = list(0. for i in range(TOTAL_CLASSES))

    # Check out why .eval() is important!
    # https://discuss.pytorch.org/t/model-train-and-model-eval-vs-model-and-model-eval/5744/2
    model.eval()

    with torch.no_grad(): # don't calculate gradient for the better calculation time in this process
      for data in dataloader: # dataloader is the input variable
          images, labels = data # data is (images, labels) data
          if is_gpu:
              images = images.cuda()
              labels = labels.cuda()
          outputs = model(Variable(images)) # autograd == Variable
          _, predicted = torch.max(outputs.data, 1) # the best class?
          predictions.extend(list(predicted.cpu().numpy()))
          total += labels.size(0)
          correct += (predicted == labels).sum() # check accuracy

          c = (predicted == labels).squeeze()
          for i in range(len(labels)):
              label = labels[i]
              class_correct[label] += c[i].cpu()
              class_total[label] += 1

    class_accuracy = 100 * np.divide(class_correct, class_total)
    return 100*correct/total, class_accuracy


def run_secret_test(dataloader, model, is_gpu):
    predictions = []
    model.eval()

    with torch.no_grad():
      for images in dataloader:
          if is_gpu:
              images = images.cuda()
          outputs = model(Variable(images)) # test
          predicted = torch.softmax(outputs, dim=1).cpu().numpy()
          predictions.extend(list(predicted))

    return predictions



# %% [markdown]
# 3. **Define a Convolution Neural Network**
# 
# Implement the BaseNet exactly. BaseNet consists of two convolutional modules (conv-relu-maxpool) and two linear layers. The precise architecture is defined below:
# 
# | Layer No.   | Layer Type  | Kernel Size | Input Dim   | Output Dim  | Input Channels | Output Channels |
# | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
# | 1 | conv2d | 5 | 32 | 28 | 3 | 6 |
# | 2 | relu | - | 28 | 28 | 6 | 6 |
# | 3 | maxpool2d | 2 | 28 | 14 | 6 | 6 |
# | 4 | conv2d | 5 | 14 | 10 | 6 | 16 |
# | 5 | relu | - | 10 | 10 | 16 | 16 |
# | 6 | maxpool2d | 2 | 10 | 5 | 16 | 16 |
# | 7 | linear | - | 1 | 1 | 400 | 200 |
# | 8 | relu | - | 1 | 1 | 200 | 200 |
# | 9 | linear | - | 1 | 1 | 200 | 10 |

# %%
########################################################################
# We provide a basic network that you should understand, run and
# eventually improve
# <<TODO>> Add more conv layers
# <<TODO>> Add more fully connected (fc) layers
# <<TODO>> Add regularization layers like Batchnorm.
#          nn.BatchNorm2d after conv layers:
#          http://pytorch.org/docs/master/nn.html#batchnorm2d
#          nn.BatchNorm1d after fc layers:
#          http://pytorch.org/docs/master/nn.html#batchnorm1d
# This is a good resource for developing a CNN for classification:
# http://cs231n.github.io/convolutional-networks/#layers

import torch.nn as nn
import torch.nn.functional as F

class BaseNetDefault(nn.Module):
    def __init__(self):
        super(BaseNet, self).__init__()

        # TODO: define your model here
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 6, kernel_size=5),  # 32x32x3 -> 28x28x6
            nn.BatchNorm2d(6),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 28x28x6 -> 14x14x6
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(6, 16, kernel_size=5),  # 14x14x6 -> 10x10x16
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 10x10x16 -> 5x5x16
        )

        # # Fully Connected Layers
        self.fc1 = nn.Sequential(
            nn.Linear(5 * 5 * 16, 200),
            nn.BatchNorm1d(200),
            nn.ReLU(),
        )

        self.fc2 = nn.Linear(200, 10)  # CIFAR-10 has 10 classes


    # def forward(self, x):
    def forward(self, x):
        bs, _, _, _ = x.shape
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(bs, -1)  # Flatten
        x = self.fc1(x)
        x = self.fc2(x)
        return x

class BaseNet(nn.Module):

    def __init__(self):
        super(BaseNet, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 32x32x3 -> 32x32x32
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # 32x32x32 -> 32x32x64
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 32x32x64 -> 16x16x64
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),  # 16x16x64 -> 16x16x128
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),  # 16x16x128 -> 16x16x128
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 16x16x128 -> 8x8x128
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),  # 8x8x128 -> 8x8x256
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),  # 8x8x256 -> 8x8x256
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 8x8x256 -> 4x4x256
        )

        # Fully Connected Layers
        self.fc1 = nn.Sequential(
            nn.Linear(4 * 4 * 256, 512),  # 4x4x256 -> 1024
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.4)  # Regularization
        )

        self.fc2 = nn.Sequential(
            nn.Linear(512, 256),  # 1024 -> 512
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.4)
        )

        self.fc3 = nn.Sequential(
            nn.Linear(256, 128),  # 1024 -> 512
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.4)
        )

        self.fc4 = nn.Linear(128, 10)  # 10 classes

    def forward(self, x):
        bs, _, _, _ = x.shape
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(bs, -1)  # Flatten
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)
        return x


# (1) Batch Normalization removed Model
class BaseNet_NoBN(nn.Module):
    def __init__(self):
        super(BaseNet_NoBN, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.fc1 = nn.Sequential(
            nn.Linear(4 * 4 * 256, 512),
            nn.ReLU(),
            nn.Dropout(0.4)
        )

        self.fc2 = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.4)
        )

        self.fc3 = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.4)
        )

        self.fc4 = nn.Linear(128, 10)

    def forward(self, x):
        bs, _, _, _ = x.shape
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(bs, -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)
        return x


# (2) Dropout Removed Model
class BaseNet_NoDropout(BaseNet):
    def __init__(self):
        super(BaseNet_NoDropout, self).__init__()

        # Remove Dropout 
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.fc1 = nn.Sequential(
            nn.Linear(4 * 4 * 256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU()
        )

        self.fc2 = nn.Sequential(
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU()
        )

        self.fc3 = nn.Sequential(
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU()
        )

        self.fc4 = nn.Linear(128, 10)

    def forward(self, x):
        bs, _, _, _ = x.shape
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(bs, -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)
        return x

# (3) Fully Connected Layer Reduced Model
class BaseNet_FC2(BaseNet):
    def __init__(self):
        super(BaseNet_FC2, self).__init__()

        # Remove Last FC Layer
        self.conv1 = BaseNet_NoDropout().conv1
        self.conv2 = BaseNet_NoDropout().conv2
        self.conv3 = BaseNet_NoDropout().conv3

        self.fc1 = nn.Sequential(
            nn.Linear(4 * 4 * 256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.4)
        )

        self.fc2 = nn.Sequential(
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.4)
        )

        self.fc4 = nn.Linear(256, 10)  # fc3 제거

    def forward(self, x):
        bs, _, _, _ = x.shape
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(bs, -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc4(x)
        return x


class BaseNet_FC1(BaseNet):
    def __init__(self):
        super(BaseNet_FC1, self).__init__()

        # Remove Last 2 FC Layer
        self.conv1 = BaseNet_NoDropout().conv1
        self.conv2 = BaseNet_NoDropout().conv2
        self.conv3 = BaseNet_NoDropout().conv3

        self.fc1 = nn.Sequential(
            nn.Linear(4 * 4 * 256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.4)
        )

        self.fc4 = nn.Linear(512, 10)  # fc2, fc3 제거
    
    def forward(self, x):
        bs, _, _, _ = x.shape
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(bs, -1)
        x = self.fc1(x)
        x = self.fc4(x)
        return x



# %%
########################################################################
# Here we use Cross-Entropy loss and SGD with momentum.
# The CrossEntropyLoss criterion already includes softmax within its
# implementation. That's why we don't use a softmax in our model
# definition.



# %% [markdown]
# | Layer No.   | Sequantial | Layer Type  | Kernel Size | Input Dim   | Output Dim  | Input Channels | Output Channels | Padding 1
# | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
# | 1 | conv1 |conv2d | 3 | 32 | 32 | 3 | 32 | 1
# | 2 | conv1 |relu | - | 32 | 32 | 32 | 32 | -
# | 3 | conv1 |conv2d | 3 | 32 | 32 | 32 | 64 | 1
# | 4 | conv1 |relu | - | 32 | 32 | 64 | 64 | -
# | 5 | conv1 |maxpool2d | 2 | 32 | 16 | 64 | 64 | 0
# | 6 | conv2 |conv2d | 3 | 16 | 16 | 64 | 128 | 1
# | 7 | conv2 |relu | - | 16 | 16 | 128 | 128 | -
# | 8 | conv2 |conv2d | 3 | 16 | 16 | 128 | 128 | 1
# | 9 | conv2 |relu | - | 16 | 16 | 128 | 128 | -
# | 10 | conv2 |maxpool2d | 2 | 16 | 8 | 128 | 128 | 0
# | 11 | conv3 |conv2d | 3 | 8 | 8 | 128 | 256 | 1
# | 12 | conv3 |relu | - | 8 | 8 | 256 | 256 | -
# | 13 | conv3 |conv2d | 3 | 8 | 8 | 256 | 256 | 1
# | 14 | conv3 |relu | - | 8 | 8 | 256 | 256 | -
# | 15 | conv3 |maxpool2d | 2 | 4 | 4 | 256 | 256 | 0
# | 16 | fc1 |Linear | - | 1 | 1 | 256 | 512 | -
# | 17 | fc1 |relu | - | 1 | 1 | 512 | 512 | -
# | 18 | fc2 |Lienar | - | 1 | 1 | 512 | 256 | -
# | 19 | fc2 |relu | - | 1 | 1 | 256 | 256 | -
# | 20 | fc3 |Linear | - | 1 | 1 | 256 | 128 | -
# | 21 | fc3 |relu | - | 1 | 1 | 128 | 128 | -
# | 22 | fc4 |Linear | - | 1 | 1 | 128 | 10 | -



# %% [markdown]
# ## Ablation Study Model

# %% [markdown]
# | Ablation Study          | BatchNorm | Dropout | FC Layers | Accuracy (%) |
# |------------------|-----------|---------|-----------|--------------|
# | BaseNet (Base Model) | YES | YES | 4       | 87           |
# | No BatchNorm     | NO   | YES | 4     | 86           |
# | No Dropout      | YES   | NO | 4       | ??           |
# | FC2 (1 Layer 제거) | YES   | YES | 2       | ??           |
# | FC1 (2 Layer 제거) | YES   | YES | 1      | ??           |



# %%
import glob
import os
import numpy as np
import random
import time
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt

import cv2
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils import data
from torchvision import models
from torchvision.transforms import ToTensor, Normalize

# %%
# global variable



# %%
class NormalDataset(data.Dataset):
    """
    Data loader for the Suface Normal Dataset. If data loading is a bottleneck,
    you may want to optimize this in for faster training. Possibilities include
    pre-loading all images and annotations into memory before training, so as
    to limit delays due to disk reads.
    """
    def __init__(self, split="train", data_dir="./taskonomy_resize_128_public"):
        assert(split in ["train", "val"])
        split2name = {
            "train": "allensville",
            "val": "beechwood",
        }
        self.img_dir = os.path.join(data_dir, split2name[split] + "_rgb")
        self.gt_dir = os.path.join(data_dir, split2name[split] + "_normal")

        self.split = split
        self.filenames = [
            os.path.splitext(os.path.basename(l))[0] for l in glob.glob(self.img_dir + "/*.png")
        ]

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, index):
        filename = self.filenames[index]
        img = Image.open(os.path.join(self.img_dir, filename) + ".png")
        img = np.asarray(img).copy()
        gt = Image.open(os.path.join(self.gt_dir, filename.replace("_rgb", "_normal")) + ".png")
        gt = np.asarray(gt)

        # from rgb image to surface normal
        gt = gt.astype(np.float32) / 255
        gt = torch.Tensor(np.asarray(gt).copy()).permute((2, 0, 1))
        mask = self.build_mask(gt).to(torch.float)

        img = ToTensor()(img)
        img = Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(img)

        # normalize gt
        gt = gt * 2 - 1

        return img.contiguous(), gt, mask.sum(dim=0) > 0

    @staticmethod
    def build_mask(target, val=0.502, tol=1e-3):
        target = target.unsqueeze(0)
        if target.shape[1] == 1:
            mask = ((target >= val - tol) & (target <= val + tol))
            mask = F.conv2d(mask.float(), torch.ones(1, 1, 5, 5, device=mask.device), padding=2) != 0
            return (~mask).expand_as(target).squeeze(0)

        mask1 = (target[:, 0, :, :] >= val - tol) & (target[:, 0, :, :] <= val + tol)
        mask2 = (target[:, 1, :, :] >= val - tol) & (target[:, 1, :, :] <= val + tol)
        mask3 = (target[:, 2, :, :] >= val - tol) & (target[:, 2, :, :] <= val + tol)
        mask = (mask1 & mask2 & mask3).unsqueeze(1)
        mask = F.conv2d(mask.float(), torch.ones(1, 1, 5, 5, device=mask.device), padding=2) != 0
        return (~mask).expand_as(target).squeeze(0)

# %% [markdown]
# # MY Model 1 - Simple Upsampling by scale factor 32

# %%
##########
#TODO: design your own network here. The expectation is to write from scratch. But it's okay to get some inspiration
#from conference paper. The bottom line is that you will not just copy code from other repo
##########

import torchvision.models as models

class MyModelDefault(nn.Module):

    def __init__(self): # feel free to modify input paramters
        super(MyModel, self).__init__()

        resnet18 = models.resnet18(weights=True)
        # self.downsample1 = nn.Sequential(*list(resnet18.children())[])
        self.my_model = nn.Sequential(*list(resnet18.children())[:-2]) # Remove the last 2 layers | total 4 layers result :  128 x 128 x 3 - > 4 x 4 x 512
        self.upsample = nn.Sequential( 
            nn.Upsample(scale_factor=32, mode='bilinear'), # 4x4x512 -> 128x128x512
            nn.Conv2d(512, 256, kernel_size=3, padding=1), # 128x128x512 -> 128x128x256
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 128, kernel_size=3, padding=1), # 128x128x256 -> 128x128x128
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 64, kernel_size=3, padding=1), # 128x128x128 -> 128x128x64
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 3, kernel_size=1) # 128x128x64 -> 128x128x3
        )

    def forward(self, *params): # feel free to modify input paramters
        # All pretrained model inputs have to be normalized
        x = self.my_model(*params)
        x = self.upsample(x)
        return x



# %% [markdown]
# # My Improved Model Getting Idea from U-net. Using Residual add from the downsampling process

# %%
##########
#TODO: design your own network here. The expectation is to write from scratch. But it's okay to get some inspiration
#from conference paper. The bottom line is that you will not just copy code from other repo
##########

import torchvision.models as models

class MyModel(nn.Module):
    def __init__(self):  # num_classes: segmentation output의 채널 수
        super(MyModel, self).__init__()

        resnet = models.resnet18(pretrained=True)

        # Encoder, Seperate the ResNet parts to work as a U - net Encoder, ResNet18 has 4 layers
        self.initial = nn.Sequential(
            resnet.conv1,  #  [8, 64, H/2, W/2] (input 128x128 ->  64x64) it has 64 kernals 
            resnet.bn1,
            resnet.relu
        ) # 128x128x3 -> 64x64x64
         
        self.maxpool = resnet.maxpool  # Reduce Spatial Resoultion (32x32x64) 

        self.layer1 = resnet.layer1  # [32x32x64]
        self.layer2 = resnet.layer2  # [16x16x128]
        self.layer3 = resnet.layer3  # [8x8x256]
        self.layer4 = resnet.layer4  # [4x4x512]

        # 128 x 128 x 3 - > 4 x 4 x 512

        # Decoder: Use ConvTranspose2d to UpSample, and use skip connection to combine encoder's feature map
        self.up4 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)  # 4x4x512 -> 8x8x256 wishing for the better resoultion!!!
        self.dec4 = nn.Sequential(
            nn.Conv2d(256 + 256, 256, kernel_size=3, padding=1), # 512 -> 256
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
        ) # skip - connection with encoder layer3 outcome

        self.up3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)  # 8x8x256 -> 16x16x128
        self.dec3 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
        )  #skip - connection with encoder layer2 outcome

        self.up2 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)  # 16x16x128 -> 32x32x64
        self.dec2 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )  # skip - connection with encoder layer1 outcome

        self.up1 = nn.ConvTranspose2d(64, 64, kernel_size=2, stride=2)  # 32x32x64 -> 64x64x64
        self.dec1 = nn.Sequential(
            nn.Conv2d(64 + 64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )
        
        # Final UpSampling: Additional Final UpSampling to make the same resolution as the input Images 64x64x32 -> 128x128x3
        self.up0 = nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2)  # 64x64x64 -> 128x128x32
        self.final_conv = nn.Conv2d(32, 3, kernel_size=1)  # Output is 3 (RGB) Channel 

    def forward(self, x):         # [8, 3, 128, 128] 
        # Encoder based on the ResNet
        x0 = self.initial(x)      # [8, 64, 64, 64] 
        x1 = self.maxpool(x0)     # [8, 64, 32, 32]
        x2 = self.layer1(x1)      # [8, 64, 32, 32]
        x3 = self.layer2(x2)      # [8, 128, 16, 16]
        x4 = self.layer3(x3)      # [8, 256, 8, 8]
        x5 = self.layer4(x4)      # [8, 512, 4, 4]

        # Decoder + skip connections
        d4 = self.up4(x5)                         # [8, 256, 8, 8]
        d4 = torch.cat([d4, x4], dim=1)             # [8, 256+256, 8, 8] d4 + x4 skip connection
        d4 = self.dec4(d4)                        # [8, 256, 8, 8]

        d3 = self.up3(d4)                         # [8, 128, 16, 16]
        # d3 = torch.cat([d3, x3], dim=1)             # [8, 128+128, 16, 16]
        d3 = self.dec3(d3)                        # [8, 128, 16, 16]

        d2 = self.up2(d3)                         # [8, 64, 32, 32]
        # d2 = torch.cat([d2, x2], dim=1)             # [8, 64+64, 32, 32]
        d2 = self.dec2(d2)                        # [8, 64, 32, 32]

        d1 = self.up1(d2)                         # [8, 64, 64, 64]
        d1 = torch.cat([d1, x0], dim=1)             # [8, 64+64, 64, 64]
        d1 = self.dec1(d1)                        # [8, 64, 64, 64]

        d0 = self.up0(d1)                         # [8, 32, 128, 128]
        out = self.final_conv(d0)                 # [8, 3 channels, 128, 128]

        return out


# %%
##########
#TODO: define your loss function here
##########
class MyCriterion(nn.Module):
    def __init__(self, alpha=1.0, beta=1.0):
        super(MyCriterion, self).__init__()
        self.l1 = nn.L1Loss()
        self.cos = nn.CosineSimilarity()
        self.alpha = alpha # To control the l1 loss
        self.beta = beta # To control the cosine similarity

    def forward(self, prediction, target, mask):
        mask = mask.unsqueeze(1)
        masked_prediction = prediction * mask
        masked_target = target * mask
        predict_error =  self.alpha * self.l1(masked_prediction, masked_target) +  self.beta * (1 - self.cos(masked_prediction, masked_target).mean())
        return predict_error

# %%
def simple_train(model, criterion, optimizer, train_dataloader, epoch, **kwargs):
    model.train()
    running_loss = 0.0
    # TODO: implement your train loop here
    for i, data in enumerate(train_dataloader, 0):
        # get the inputs
        inputs, labels, mask = data

        if IS_GPU:
            inputs = inputs.cuda()
            labels = labels.cuda()
            mask = mask.cuda()

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(inputs)
        loss = criterion(outputs, labels, mask)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
    epoch_loss = running_loss / len(train_dataloader)
    print(f"Epoch [{epoch+1}], Loss: {epoch_loss:.4f}")

    val_gts, val_preds, val_losses, val_total_normal_errors = simple_predict('val', model)
    print("Validation loss (L1):", np.mean(val_losses))
    print("Validation metrics: Mean %.1f, Median %.1f, 11.25deg %.1f, 22.5deg %.1f, 30deg %.1f" % (
        np.average(val_total_normal_errors), np.median(val_total_normal_errors),
        np.sum(val_total_normal_errors < 11.25) / val_total_normal_errors.shape[0] * 100,
        np.sum(val_total_normal_errors < 22.5) / val_total_normal_errors.shape[0] * 100,
        np.sum(val_total_normal_errors < 30) / val_total_normal_errors.shape[0] * 100
    ))
        


# %% [markdown]
# | Loss Function | Mean AE (°) ↓ | Median AE (°) ↓ | Acc @ 11.25° (%) ↑ | Acc @ 22.5° (%) ↑ | Acc @ 30° (%) ↑ | 
# |--------------|----------|--------------------|--------------------|--------------------|----------|
# | Baseline (α=1.0, β=1.0) | 42.5 | 38.6 | 15.1 | 31.3 | 40.5 |
# | More Cosine Similarity (α=0.5, β=1.5) | 43.6 | 39.8 | 13.7 | 30.1 | 39.3 |
# | More L1 Loss (α=1.5, β=0.5) | 41.7 | 38.1 | 14.9 | 31.1 | 40.6 |
# | Balanced High Weights (α=2.0, β=2.0) | 40.0 | 36.1 | 14.8 | 32.1 | 42.3 |
# | Balanced Higher Weights (α=5.0, β=5.0) | 38.0 | 34.4 | 17.4 | 34.9 | 44.8 |

# %% [markdown]
# | Skip Connection Variant | MAE (°) ↓ | Median AE (°) ↓ | Acc @ 11.25° (%) ↑ | Acc @ 22.5° (%) ↑ | Acc @ 30° (%) ↑ | 
# |------------------------|----------|--------------------|--------------------|--------------------|----------|
# | Baseline (Full U-Net) | 38.0 | 34.4 | 17.4 | 34.9 | 44.8 |
# | Removing Early Skip (Skip1) | 37.4 | 32.9 | 19.4 | 36.9 | 46.6 |
# | Removing Late Skip (Skip4) | 38.1 | 34.1 | 18.6 | 35.3 | 44.9 |
# | Fewer Skip Connections (Keep Only Skip2,3) | 35.9 | 32.2 | 15.9 | 35.3 | 46.9 |

# %% [markdown]
# # You do not need to change anything below

# %%
########################################################################
# Evaluate your result, and report
# 1. Mean angular error
# 2. Median angular error
# 3. Accuracy at 11.25 degree
# 4. Accuracy at 22.5 degree
# 5. Accuracy at 30 degree
# using provided `simple_predict` function.

def angle_error(prediction, target):
    prediction_error = torch.cosine_similarity(prediction, target)
    prediction_error = torch.clamp(prediction_error, min=-1.0, max=1.0)
    prediction_error = torch.acos(prediction_error) * 180.0 / np.pi
    return prediction_error

def simple_predict(split, model):
    model.eval()
    dataset = NormalDataset(split=split)
    dataloader = data.DataLoader(dataset, batch_size=1, shuffle=False,
                                 num_workers=2, drop_last=False)
    gts, preds, losses = [], [], []
    total_normal_errors = None
    with torch.no_grad():
        for i, batch in enumerate(tqdm(dataloader)):
            img, gt, mask = batch
            img = img.to(device)
            gt = gt.to(device)
            mask = mask.to(device)

            pred = model(img)
            loss = (F.l1_loss(pred, gt, reduction="none") * mask.unsqueeze(1)).mean()

            gts.append((gt[0].permute((1, 2, 0)).cpu().numpy() + 1) / 2)
            preds.append((pred[0].permute((1, 2, 0)).cpu().numpy() + 1) / 2)
            losses.append(loss.item())

            angle_error_prediction = angle_error(pred, gt)
            angle_error_prediction = angle_error_prediction[mask > 0].view(-1)
            if total_normal_errors is None:
                total_normal_errors = angle_error_prediction.cpu().numpy()
            else:
                total_normal_errors = np.concatenate(
                    (total_normal_errors, angle_error_prediction.cpu().numpy())
                )

    return gts, preds, losses, total_normal_errors



# %%
# Visualization
# pick some of your favorite images and put them under `./data/normal_visualization/image`

class VisualizationDataset(data.Dataset):
    def __init__(self, image_dir="./taskonomy_resize_128_public", image_ext=".png"):
        self.img_dir = image_dir
        self.img_ext = image_ext

        self.img_dir = os.path.join(image_dir, "collierville_rgb")

        self.image_filenames = [
            os.path.splitext(os.path.basename(l))[0] for l in glob.glob(self.img_dir + "/*" + image_ext)
        ]

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, index):
        filename = self.image_filenames[index]
        img = Image.open(os.path.join(self.img_dir, filename) + self.img_ext)
        img = np.asarray(img).copy()
        img = ToTensor()(img)
        img = Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(img)

        return img.contiguous(), filename

def simple_vis(model):
    model.eval()
    dataset = VisualizationDataset(image_dir="./taskonomy_resize_128_public")
    dataloader = data.DataLoader(dataset, batch_size=1, shuffle=False,
                                 num_workers=2, drop_last=False)
    imgs, preds = [], []

    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    with torch.no_grad():
        for i, batch in enumerate(tqdm(dataloader)):
            img, _ = batch
            img = img.to(device)

            pred = model(img)
            imgs.append(
                std * img[0].permute((1, 2, 0)).cpu().numpy() + mean
            )
            preds.append((pred[0].permute((1, 2, 0)).cpu().numpy() + 1) / 2)

    return imgs, preds



# %%
# Test your model on the test set, submit the output to gradescope

from PIL import Image
import numpy as np

def simple_test(model, out_dir):
    model.eval()
    dataset = VisualizationDataset(image_dir="./taskonomy_resize_128_public")
    dataloader = data.DataLoader(dataset, batch_size=1, shuffle=False,
                                 num_workers=2, drop_last=False)

    saved_predictions = []
    with torch.no_grad():
        for i, batch in enumerate(tqdm(dataloader)):
            img, filename = batch
            img = img.to(device)

            pred = model(img)
            saved_predictions.append(pred.cpu())

        saved_predictions = torch.cat(saved_predictions, dim=0)
        return saved_predictions


