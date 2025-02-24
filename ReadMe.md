- [My ZhiHu column](#my-zhihu-column)
- [Introduction](#introduction)
- [Environments](#environments)
- [Download datasets and my pretrained models](#download-datasets-and-my-pretrained-models)
- [Prepare datasets](#prepare-datasets)
- [Train and test model](#train-and-test-model)
- [Contrastive learning training results](#contrastive-learning-training-results)
  - [ILSVRC2012(ImageNet) pretrained results](#ilsvrc2012imagenet-pretrained-results)
  - [ILSVRC2012(ImageNet) finetune results](#ilsvrc2012imagenet-finetune-results)
- [Masked image modeling training results](#masked-image-modeling-training-results)
  - [ILSVRC2012(ImageNet) pretrained results](#ilsvrc2012imagenet-pretrained-results)
  - [ILSVRC2012(ImageNet) finetune results](#ilsvrc2012imagenet-finetune-results)
- [Classification training results](#classification-training-results)
  - [ILSVRC2012(ImageNet) training results](#ilsvrc2012imagenet-training-results)
  - [CIFAR100 training results](#cifar100-training-results)
- [Detection training results](#detection-training-results)
  - [COCO2017 training results](#coco2017-training-results)
  - [VOC2007 and VOC2012 training results](#voc2007-and-voc2012-training-results)
- [Semantic Segmentation training results](#semantic-segmentation-training-results)
  - [ADE20K training results](#ade20k-training-results)
- [Distillation training results](#distillation-training-results)
  - [ImageNet training results](#imagenet-training-results)
- [Citation](#citation)


# My ZhiHu column

https://www.zhihu.com/column/c_1249719688055193600

# Introduction

This repository provides simple training and testing examples for image classification, object detection, semantic segmentation, knowledge distillation, contrastive learning, masked image modeling training.

**contrastive learning**
```
DINO(for ResNet50)
```

**masked image modeling training**
```
MAE(for ViT_Base_Patch16)
```

**image classification:**
```
ResNet
DarkNet
RepVGG
RegNetX
```

**object detection:**
```
RetinaNet
FCOS
CenterNet
TTFNet
```

**semantic segmentation:**
```
DeepLabv3+
Segmenter
```

**knowledge distillation:**
```
KD loss
DKD loss
DML loss
```

# Environments

**This repository only support one server one gpu card/one server multi gpu cards.**

**environments:**

Ubuntu 20.04.3 LTS,30 core AMD EPYC 7543 32-Core Processor, 2*RTX A5000, Python Version:3.8, CUDA Version:11.3

Please make sure your Python version>=3.7.

**Use pip or conda to install those Packages:**
```
torch==1.10.0
torchvision==0.11.1
torchaudio==0.10.0
onnx==1.11.0
onnx-simplifier==0.3.6
numpy
Cython
pycocotools
opencv-python
tqdm
thop==0.0.31.post2005241907
yapf
apex
```

**How to install apex?**

apex needs to be installed separately.First,download apex：
```
git clone https://github.com/NVIDIA/apex
```

For torch1.10,modify apex/apex/amp/utils.py:
```
if cached_x.grad_fn.next_functions[1][0].variable is not x:
```
to
```
if cached_x.grad_fn.next_functions[0][0].variable is not x:
```

Then use the following orders to install apex:
```
cd apex
pip install -v --no-cache-dir ./
```
Using apex to train can reduce video memory usage by 25%-30%, but the training speed will be slower, the trained model has the same performance as not using apex.

# Download datasets and my pretrained models

You can download all datasets、all my pretrained models and all my experiments records/checkpoints from Baidu-Netdisk:
```
# all datasets
链接：https://pan.baidu.com/s/16fAq74UMe6M1FVO_IDbqgA 
提取码：vtm8
# all my pretrained models
链接：https://pan.baidu.com/s/1j7jm3I-UpMH7lJUOmJxhqg 
提取码：okm8
# all my experiments records/checkpoints
链接：https://pan.baidu.com/s/17yT6m98lXi9gXYgIK5afyw 
提取码：ofc0
```

# Prepare datasets

If you want to reproduce my imagenet pretrained models,you need download ILSVRC2012 dataset,and make sure the folder architecture as follows:
```
ILSVRC2012
|
|-----train----1000 sub classes folders
|-----val------1000 sub classes folders
Please make sure the same class has same class folder name in train and val folders.
```

If you want to reproduce my cifar100 pretrained models,you need download cifar100 dataset,and make sure the folder architecture as follows:
```
CIFAR100
|
|-----train unzip from cifar-100-python.tar.gz
|-----test  unzip from cifar-100-python.tar.gz
|-----meta  unzip from cifar-100-python.tar.gz
```

If you want to reproduce my COCO2017 pretrained models,you need download COCO2017 dataset,and make sure the folder architecture as follows:
```
COCO2017
|                |----captions_train2017.json
|                |----captions_val2017.json
|--annotations---|----instances_train2017.json
|                |----instances_val2017.json
|                |----person_keypoints_train2017.json
|                |----person_keypoints_val2017.json
|                 
|                |----train2017
|----images------|----val2017
```

If you want to reproduce my VOC2007/VOC2012 pretrained models,you need download VOC2007+VOC2012 dataset,and make sure the folder architecture as follows:
```
VOCdataset
|                 |----Annotations
|                 |----ImageSets
|----VOC2007------|----JPEGImages
|                 |----SegmentationClass
|                 |----SegmentationObject
|        
|                 |----Annotations
|                 |----ImageSets
|----VOC2012------|----JPEGImages
|                 |----SegmentationClass
|                 |----SegmentationObject
```

If you want to reproduce my ADE20K pretrained models,you need download ADE20K dataset,and make sure the folder architecture as follows:
```
ADE20K
|                 |----training
|---images--------|----validation
|                 |----testing
|        
|                 |----training
|---annotations---|----validation
```

# Train and test model

If you want to train or test model,you need enter a training folder directory,then run train.sh and test.sh.

For example,you can enter classification_training/imagenet/resnet50.

If you want to train this model from scratch,please delete checkpoints and log folders first,then run train.sh:
```
CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.run --nproc_per_node=2 --master_addr 127.0.1.0 --master_port 10000 ../../../tools/train_classification_model.py --work-dir ./
```

CUDA_VISIBLE_DEVICES is used to specify the gpu ids for this training.Please make sure the number of nproc_per_node equal to the number of gpu cards.Make sure master_addr/master_port are unique for each training.

if you want to test this model,you need have a pretrained model first,modify trained_model_path in test_config.py,then run test.sh:
```
CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.run --nproc_per_node=2 --master_addr 127.0.1.0 --master_port 10000 ../../../tools/test_classification_model.py --work-dir ./
```
Also, You can modify super parameters in train_config.py/test_config.py.


If you see the following log, and train.sh/test.sh keeps running, then train.sh/test.sh is running correctly.

All checkpoints/log are saved in training/testing folder directory.
```
Warning:  apex was installed without --cpp_ext.  Falling back to Python flatten and unflatten.
Selected optimization level O1:  Insert automatic casts around Pytorch functions and Tensor methods.

Defaults for this optimization level are:
enabled                : True
opt_level              : O1
cast_model_type        : None
patch_torch_functions  : True
keep_batchnorm_fp32    : None
master_weights         : None
loss_scale             : dynamic
Processing user overrides (additional kwargs that are not None)...
After processing overrides, optimization options are:
enabled                : True
opt_level              : O1
cast_model_type        : None
patch_torch_functions  : True
keep_batchnorm_fp32    : None
master_weights         : None
loss_scale             : dynamic
Warning:  multi_tensor_applier fused unscale kernel is unavailable, possibly because apex was installed without --cuda_ext --cpp_ext. Using Python fallback.
Original ImportError was: ModuleNotFoundError("No module named 'amp_C'")
Warning:  apex was installed without --cpp_ext.  Falling back to Python flatten and unflatten.
```

# Contrastive learning training results

**DINO:Emerging Properties in Self-Supervised Vision Transformers**

Paper:https://arxiv.org/abs/2104.14294

## ILSVRC2012(ImageNet) pretrained results
| Network | input size | gpu num | batch | epochs | Loss |
| ------- | ---------- | ------- | ----- | ------ | ---- |
| ResNet50_dino_pretrained_epoch100 | 224x224 | 2 RTX A5000 | 128 | 100 | 2.4567 |

## ILSVRC2012(ImageNet) finetune results
| Network | macs | params | input size | gpu num | batch | epochs | Top-1  |
| ------- | ---- | ------ | ---------- | ------- | ----- | ------ | -----  |
| ResNet50_finetune_epoch100_dino_pretrained_epoch_100 | 4.112G | 25.557M | 224x224 | 2 RTX A5000 | 256 | 100 | 76.858 |

# Masked image modeling training results

**MAE:Masked Autoencoders Are Scalable Vision Learners**

Paper:https://arxiv.org/abs/2111.06377

**VIT:An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale**

Paper:https://arxiv.org/abs/2010.11929

## ILSVRC2012(ImageNet) pretrained results
| Network | input size | gpu num | batch | epochs | Loss |
| ------- | ---------- | ------- | ----- | ------ | ---- |
| ViT_Base_Patch16_mae_pretrained_epoch100 | 224x224 | 2 RTX A5000 | 256x4 | 100 | 0.3986 |
| ViT_Base_Patch16_mae_pretrained_epoch400 | 224x224 | 2 RTX A5000 | 256x4 | 400 | 0.3879 |

## ILSVRC2012(ImageNet) finetune results
| Network | macs | params | input size | gpu num | batch | epochs | Top-1  |
| ------- | ---- | ------ | ---------- | ------- | ----- | ------ | -----  |
| ViT_Base_Patch16_finetune_epoch100_mae_pretrained_epoch_100 | 16.849G | 86.377M | 224x224 | 2 RTX A5000 | 256x4 | 100 | 82.182 |
| ViT_Base_Patch16_finetune_epoch100_mae_pretrained_epoch_400 | 16.849G | 86.377M | 224x224 | 2 RTX A5000 | 256x4 | 100 | 83.130 |

# Classification training results

**ResNet**

Paper:https://arxiv.org/abs/1512.03385

**DarkNet**

Paper:https://arxiv.org/abs/1804.02767?e05802c1_page=1

**RepVGG**

Paper:https://arxiv.org/abs/2101.03697

**RegNet**

Paper:https://arxiv.org/abs/2003.13678

## ILSVRC2012(ImageNet) training results

| Network | macs | params | input size | gpu num | batch | epochs | Top-1  |
| ------- | ---- | ------ | ---------- | ------- | ----- | ------ | -----  |
| ResNet18     | 1.819G   | 11.690M     | 224x224    | 2 RTX A5000  | 256       | 100    | 70.712 |
| ResNet34half | 949.323M | 5.585M      | 224x224    | 2 RTX A5000  | 256       | 100    | 67.752 |
| ResNet34     | 3.671G   | 21.798M     | 224x224    | 2 RTX A5000  | 256       | 100    | 73.752 |
| ResNet50half | 1.063G   | 6.918M      | 224x224    | 2 RTX A5000  | 256       | 100    | 72.902 |
| ResNet50     | 4.112G   | 25.557M     | 224x224    | 2 RTX A5000  | 256       | 100    | 76.264 |
| ResNet101    | 7.834G   | 44.549M     | 224x224    | 2 RTX A5000  | 256       | 100    | 77.322 |
| ResNet152    | 11.559G  | 60.193M     | 224x224    | 2 RTX A5000  | 256       | 100    | 78.006 |
| DarkNetTiny  | 412.537M | 2.087M      | 256x256    | 2 RTX A5000  | 256       | 100    | 57.602 |
| DarkNet19    | 3.663G   | 20.842M     | 256x256    | 2 RTX A5000  | 256       | 100    | 74.028 |
| DarkNet53    | 9.322G   | 41.610M     | 256x256    | 2 RTX A5000  | 256       | 100    | 76.602 |
| RepVGG_A0_deploy | 1.362G   | 8.309M      | 224x224    | 2 RTX A5000  | 256   | 120    | 72.156 |
| RepVGG_A1_deploy | 2.364G   | 12.790M     | 224x224    | 2 RTX A5000  | 256   | 120    | 74.056 |
| RepVGG_A2_deploy | 5.117G   | 25.500M     | 224x224    | 2 RTX A5000  | 256   | 120    | 76.022 |
| RepVGG_B0_deploy | 3.058G   | 14.339M     | 224x224    | 2 RTX A5000  | 256   | 120    | 74.750 |
| RepVGG_B1_deploy | 11.816G  | 51.829M     | 224x224    | 2 RTX A5000  | 256   | 120    | 77.834 |
| RepVGG_B2_deploy | 18.377G  | 80.315M     | 224x224    | 2 RTX A5000  | 256   | 120    | 78.226 |
| RegNetX_400MF    | 410.266M | 5.158M      | 224x224    | 2 RTX A5000  | 256   | 100    | 72.364 |
| RegNetX_600MF    | 616.813M | 6.196M      | 224x224    | 2 RTX A5000  | 256   | 100    | 73.598 |
| RegNetX_800MF    | 820.324M | 7.260M      | 224x224    | 2 RTX A5000  | 256   | 100    | 74.444 |
| RegNetX_1_6GF    | 1.635G   | 9.190M      | 224x224    | 2 RTX A5000  | 256   | 100    | 76.580 |
| RegNetX_3_2GF    | 3.222G   | 15.297M     | 224x224    | 2 RTX A5000  | 256   | 100    | 77.512 |
| RegNetX_4_0GF    | 4.013G   | 22.118M     | 224x224    | 2 RTX A5000  | 256   | 100    | 77.722 |

You can find more model training details in classification_training/imagenet/.

## CIFAR100 training results

| Network | macs | params | input size | gpu num | batch | epochs | Top-1  |
| ------- | ---- | ------ | ---------- | ------- | ----- | ------ | -----  |
| ResNet18Cifar     | 557.935M | 11.220M     | 32x32      | 1 RTX A5000  | 128  | 200    | 76.730 |
| ResNet34halfCifar | 292.370M | 5.350M      | 32x32      | 1 RTX A5000  | 128  | 200    | 75.730 |
| ResNet34Cifar     | 1.164G   | 21.328M     | 32x32      | 1 RTX A5000  | 128  | 200    | 77.850 |
| ResNet50halfCifar | 331.879M | 5.991M      | 32x32      | 1 RTX A5000  | 128  | 200    | 75.880 |
| ResNet50Cifar     | 1.312G   | 23.705M     | 32x32      | 1 RTX A5000  | 128  | 200    | 75.890 |
| ResNet101Cifar    | 2.531G   | 42.697M     | 32x32      | 1 RTX A5000  | 128  | 200    | 79.710 |
| ResNet152Cifar    | 3.751G   | 58.341M     | 32x32      | 1 RTX A5000  | 128  | 200    | 77.150 |

You can find more model training details in classification_training/cifar100/.

# Detection training results

**RetinaNet**

Paper:https://arxiv.org/abs/1708.02002

**FCOS**

Paper:https://arxiv.org/abs/1904.01355

**CenterNet**

Paper:https://arxiv.org/abs/1904.07850

**TTFNet**

Paper:https://arxiv.org/abs/1909.00700

**YOLOX**

Paper:https://arxiv.org/abs/2107.08430

**How to use yolov3 anchor clustering method to generate a set of custom anchors for your own dataset?**

I provide a script in simpleAICV/detection/yolov3_anchor_cluster.py,and I give two examples for generate anchors on COCO2017 and VOC2007+2012 datasets.If you want to generate anchors for your dataset,just modify the part of input code,get width and height of all annotaion boxes,then use the script to compute anchors.The anchors size will change with different datasets or different input resizes.

## COCO2017 training results

Trained on COCO2017_train dataset, tested on COCO2017_val dataset.

mAP is IoU=0.5:0.95,area=all,maxDets=100,mAP(COCOeval,stats[0]).

| Network | resize-style | input size | macs | params | gpu num | batch | epochs | mAP |
| ------- | ------------ | ---------- | ---- | ------ | ------- | ----- | ------ | --- |
| ResNet50-RetinaNet    | RetinaStyle-400 | 400x667    | 63.093G  | 37.969M  | 2 RTX A5000  | 32        | 13     | 31.939 |
| ResNet50-RetinaNet    | RetinaStyle-800 | 800x1333   | 250.069G | 37.969M  | 2 RTX A5000  | 8         | 13     | 35.082 |
| ResNet50-RetinaNet    | YoloStyle-640   | 640x640    | 95.558G  | 37.969M  | 2 RTX A5000  | 32        | 13     | 33.475 |
| ResNet101-RetinaNet   | RetinaStyle-800 | 800x1333   | 329.836G | 56.961M  | 2 RTX A5000  | 8         | 13     | 36.406 |
| ResNet50-FCOS         | RetinaStyle-400 | 400x667    | 54.066G  | 32.291M  | 2 RTX A5000  | 32        | 13     | 34.671 |
| ResNet50-FCOS         | RetinaStyle-800 | 800x1333   | 214.406G | 32.291M  | 2 RTX A5000  | 8         | 13     | 37.850 |
| ResNet50-FCOS         | YoloStyle-640   | 640x640    | 81.943G  | 32.291M  | 2 RTX A5000  | 32        | 13     | 35.629 |
| ResNet101-FCOS        | RetinaStyle-800 | 800x1333   | 294.173G | 51.283M  | 2 RTX A5000  | 8         | 13     | 39.547 |
| vit_base_patch16_fcos | YoloStyle-640 | 640x640 | 184.171G | 91.506M  | 2 RTX A5000  | 8         | 13     | 39.948 |
| ResNet18DCN-CenterNet | YoloStyle-512   | 512x512    | 14.854G  | 12.889M  | 2 RTX A5000  | 64        | 140    | 27.947 |
| ResNet18DCN-TTFNet-3x | YoloStyle-512   | 512x512    | 16.063G  | 13.737M  | 2 RTX A5000  | 64        | 39     | 27.847 |

You can find more model training details in detection_training/coco/.

## VOC2007 and VOC2012 training results

Trained on VOC2007 trainval dataset + VOC2012 trainval dataset, tested on VOC2007 test dataset.

mAP is IoU=0.50,area=all,maxDets=100,mAP.

| Network | resize-style | input size | macs | params | gpu num | batch | epochs | mAP |
| ------- | ------------ | ---------- | ---- | ------ | ------- | ----- | ------ | --- |
| ResNet50-RetinaNet    | YoloStyle-640   | 640x640    | 84.947G  | 36.724M  | 2 RTX A5000  | 32        | 13     | 80.693 |
| ResNet50-FCOS         | YoloStyle-640   | 640x640    | 80.764G  | 32.153M  | 2 RTX A5000  | 32        | 13     | 79.960 |

You can find more model training details in detection_training/voc/.

# Semantic Segmentation training results

**DeepLabv3+**

Paper:https://arxiv.org/abs/1802.02611

**Segmenter**

Paper:https://arxiv.org/abs/2105.05633

## ADE20K training results

| Network             | input size | macs    | params  | gpu num     | batch | epochs | miou |
| ------------------- | ---------- | ------- | ------- | ----------- | ----- | ------ | ---- |
| ResNet50-DeepLabv3+        | 512x512    | 25.548G  | 26.738M  | 2 RTX A5000 | 8     | 128    | 34.058 |
| vit_base_patch16_Segmenter_mae_pretrain_epoch400 | 512x512    | 104.886G | 100.368M | 2 RTX A5000 | 8     | 128    | 40.652 |
| vit_base_patch16_Segmenter_cls_pretrain_83.130 | 512x512    | 104.886G | 100.368M | 2 RTX A5000 | 8     | 128    | 42.058 |


# Distillation training results

**KD loss**

Paper:https://arxiv.org/abs/1503.02531

**DKD loss**

Paper:https://arxiv.org/abs/2203.08679

**DML loss**

Paper:https://arxiv.org/abs/1706.00384

## ImageNet training results

| Teacher Network  | Student Network  | method  | Freeze Teacher | input size | gpu num      | batch     | epochs | Teacher Top-1  | Student Top-1  |
| ---------------- | ---------------- | ------- | -------------- | ---------- | ------------ | --------- | ------ | ---------------  | ------------ |
| ResNet34         | ResNet18         | CE+KD   | True           | 224x224    | 2 RTX A5000  | 256       | 100    | /              | 71.984         |
| ResNet34         | ResNet18         | CE+DKD  | True           | 224x224    | 2 RTX A5000  | 256       | 100    | /              | 72.110         |
| ResNet34         | ResNet18         | CE+DML  | False          | 224x224    | 2 RTX A5000  | 256       | 100    | 74.674         | 72.064         |
| ResNet152        | ResNet50         | CE+KD   | True           | 224x224    | 2 RTX A5000  | 256       | 100    | /              | 76.476         |
| ResNet152        | ResNet50         | CE+DKD  | True           | 224x224    | 2 RTX A5000  | 256       | 100    | /              | 77.616         |
| ResNet152        | ResNet50         | CE+DML  | False          | 224x224    | 2 RTX A5000  | 256       | 100    | 79.148         | 77.622         |

You can find more model training details in distillation_training/imagenet/.

# Citation

If you find my work useful in your research, please consider citing:
```
@inproceedings{zgcr,
 title={SimpleAICV-ImageNet-CIFAR-COCO-VOC-training},
 author={zgcr},
 year={2022}
}
```