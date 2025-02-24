import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)

from tools.path import ILSVRC2012_path

from simpleAICV.classification import backbones
from simpleAICV.classification import losses
from simpleAICV.classification.datasets.ilsvrc2012dataset import ILSVRC2012Dataset
from simpleAICV.classification.common import Normalize, CenterCrop, MeanStdNormalize, ClassificationCollater, load_state_dict

import torch
import torchvision.transforms as transforms


class config:
    '''
    for resnet,input_image_size = 224;for darknet,input_image_size = 256
    '''
    network = 'RegNetX_400MF'
    num_classes = 1000
    input_image_size = 224
    scale = 256 / 224

    model = backbones.__dict__[network](**{
        'num_classes': num_classes,
    })

    # load pretrained model or not
    trained_model_path = '/root/code/SimpleAICV-ImageNet-CIFAR-COCO-VOC-training/classification_training/imagenet/regnetx_400mf/checkpoints/RegNetX_400MF-acc72.376.pth'
    # trained_model_path = os.path.join(BASE_DIR, '')
    load_state_dict(trained_model_path, model)

    test_criterion = losses.__dict__['CELoss']()

    test_dataset = ILSVRC2012Dataset(
        root_dir=ILSVRC2012_path,
        set_name='val',
        transform=transforms.Compose([
            Normalize(),
            CenterCrop(scale_size=input_image_size * scale,
                       crop_size=input_image_size),
            MeanStdNormalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
        ]))
    test_collater = ClassificationCollater()

    seed = 0
    # batch_size is total size
    batch_size = 256
    # num_workers is total workers
    num_workers = 16