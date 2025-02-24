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
    network = 'yoloxm'
    num_classes = 80
    input_image_size = [640, 640]

    model = models.__dict__[network](**{
        'backbone_pretrained_path': '',
        'num_classes': num_classes,
    })

    # load total pretrained model or not
    trained_model_path = ''
    load_state_dict(trained_model_path, model)

    test_criterion = losses.__dict__['YoloxLoss'](**{
        'strides': [8, 16, 32],
        'obj_loss_weight': 1.0,
        'box_loss_weight': 5.0,
        'cls_loss_weight': 1.0,
        'box_loss_iou_type': 'CIoU',
        'center_sample_radius': 2.5,
    })

    decoder = decode.__dict__['YoloxDecoder'](**{
        'strides': [8, 16, 32],
        'max_object_num': 100,
        'min_score_threshold': 0.05,
        'topn': 1000,
        'nms_type': 'python_nms',
        'nms_threshold': 0.6,
    })

    test_dataset = CocoDetection(COCO2017_path,
                                 set_name='val2017',
                                 transform=transforms.Compose([
                                     YoloStyleResize(
                                         resize=input_image_size[0],
                                         divisor=32,
                                         stride=32,
                                         multi_scale=False,
                                         multi_scale_range=[0.5, 1.0]),
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
    batch_size = 32
    # num_workers is total workers
    num_workers = 20