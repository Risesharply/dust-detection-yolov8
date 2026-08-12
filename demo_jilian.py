# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
import argparse
import os
import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import torch
import torch.backends.cudnn as cudnn
import tensorflow as tf

ROOT_YOLOV5 = Path('./yolov5')
ROOT_EFFICIENTNETV2 = Path('automl/efficientnetv2')

if str(ROOT_YOLOV5) not in sys.path and str(ROOT_EFFICIENTNETV2) not in sys.path:
    sys.path.insert(0, str(ROOT_YOLOV5))
else:
    sys.path[0] = str(ROOT_YOLOV5)

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, \
    increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync

