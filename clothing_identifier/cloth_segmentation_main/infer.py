import os

from tqdm import tqdm
from PIL import Image
import numpy as np

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import torch
import torch.nn.functional as F
import torchvision.transforms as transforms

from .data.base_dataset import Normalize_image
from .utils.saving_utils import load_checkpoint_mgpu

from .networks import U2NET


from pathlib import Path

from ..forms import *


def get_palette(num_cls):
    """Returns the color map for visualizing the segmentation mask.
    Args:
        num_cls: Number of classes
    Returns:
        The color map
    """
    n = num_cls
    palette = [0] * (n * 3)
    for j in range(0, n):
        lab = j
        palette[j * 3 + 0] = 0
        palette[j * 3 + 1] = 0
        palette[j * 3 + 2] = 0
        i = 0
        while lab:
            palette[j * 3 + 0] |= ((lab >> 0) & 1) << (7 - i)
            palette[j * 3 + 1] |= ((lab >> 1) & 1) << (7 - i)
            palette[j * 3 + 2] |= ((lab >> 2) & 1) << (7 - i)
            i += 1
            lab >>= 3
    return palette



def generateOutput(image_dir,result_dir) :

    device = "cpu"

    # image_dir = os.path.join(Path(__file__).resolve().parent, "input_images")

    # result_dir = os.path.join(Path(__file__).resolve().parent, "output_images")

    checkpoint_path = os.path.join(Path(__file__).resolve().parent, "cloth_segm_u2net_latest.pth")
    do_palette = True


    transforms_list = []
    transforms_list += [transforms.ToTensor()]
    transforms_list += [Normalize_image(0.5, 0.5)]
    transform_rgb = transforms.Compose(transforms_list)

    net = U2NET(in_ch=3, out_ch=4)
    net = load_checkpoint_mgpu(net, checkpoint_path)
    net = net.to(device)
    net = net.eval()

    palette = get_palette(4)

    pbar = tqdm(total=1)
    img = Image.open(image_dir).convert("RGB")
    image_tensor = transform_rgb(img)
    image_tensor = torch.unsqueeze(image_tensor, 0)

    output_tensor = net(image_tensor.to(device))
    output_tensor = F.log_softmax(output_tensor[0], dim=1)
    output_tensor = torch.max(output_tensor, dim=1, keepdim=True)[1]
    output_tensor = torch.squeeze(output_tensor, dim=0)
    output_tensor = torch.squeeze(output_tensor, dim=0)
    output_arr = output_tensor.cpu().numpy()

    output_img = Image.fromarray(output_arr.astype("uint8"), mode="L")
    if do_palette:
        output_img.putpalette(palette)
    # output_img.save(result_dir[:-3]+"png")
    output_img.save(result_dir)
    # try :
    #    tempImage.image = tempImage.image.url[:-3]+"png"
    #    tempImage.save()
    # except Exception as e :
    #     print(e," updating output")
    #     outputImageObject = None

    pbar.update(1)

    pbar.close()

    # return outputImageObject
# generateOutput(os.path.join(Path(__file__).resolve().parent, "input_images"))