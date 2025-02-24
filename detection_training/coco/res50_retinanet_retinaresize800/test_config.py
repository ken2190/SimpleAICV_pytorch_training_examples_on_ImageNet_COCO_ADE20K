import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)

from tools.path import COCO2017_path

from simpleAICV.detection import models
from simpleAICV.detection import losses
from simpleAICV.detection import decode
from simpleAICV.detection.datasets.cocodataset import CocoDetection
from simpleAICV.detection.common import RetinaStyleResize, YoloStyleResize, RandomHorizontalFlip, Normalize, DetectionCollater, load_state_dict

import torch
import torchvision.transforms as transforms


class config:
    network = 'resnet50_retinanet'
    num_classes = 80
    input_image_size = [800, 1333]

    model = models.__dict__[network](**{
        'backbone_pretrained_path': '',
        'num_classes': num_classes,
    })

    # load total pretrained model or not
    trained_model_path = '/root/code/SimpleAICV-ImageNet-CIFAR-COCO-VOC-training/detection_training/coco/res50_retinanet_retinaresize800/checkpoints/resnet50_retinanet-metric35.077.pth'
    # trained_model_path = os.path.join(BASE_DIR, '')
    load_state_dict(trained_model_path, model)

    test_criterion = losses.__dict__['RetinaLoss'](
        **{
            'areas': [[32, 32], [64, 64], [128, 128], [256, 256], [512, 512]],
            'ratios': [0.5, 1, 2],
            'scales': [2**0, 2**(1.0 / 3.0), 2**(2.0 / 3.0)],
            'strides': [8, 16, 32, 64, 128],
            'alpha': 0.25,
            'gamma': 2,
            'beta': 1.0 / 9.0,
            'focal_eiou_gamma': 0.5,
            'cls_loss_weight': 1.,
            'box_loss_weight': 1.,
            'box_loss_type': 'CIoU',
        })

    decoder = decode.__dict__['RetinaDecoder'](
        **{
            'areas': [[32, 32], [64, 64], [128, 128], [256, 256], [512, 512]],
            'ratios': [0.5, 1, 2],
            'scales': [2**0, 2**(1.0 / 3.0), 2**(2.0 / 3.0)],
            'strides': [8, 16, 32, 64, 128],
            'max_object_num': 100,
            'min_score_threshold': 0.05,
            'topn': 1000,
            'nms_type': 'python_nms',
            'nms_threshold': 0.5,
        })

    test_dataset = CocoDetection(COCO2017_path,
                                 set_name='val2017',
                                 transform=transforms.Compose([
                                     RetinaStyleResize(
                                         resize=input_image_size[0],
                                         divisor=32,
                                         stride=32,
                                         multi_scale=False,
                                         multi_scale_range=[0.8, 1.0]),
                                     Normalize(),
                                 ]))
    test_collater = DetectionCollater()

    # 'COCO' or 'VOC'
    eval_type = 'COCO'
    eval_voc_iou_threshold_list = [
        0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95
    ]

    seed = 0
    # batch_size is total size
    batch_size = 8
    # num_workers is total workers
    num_workers = 16