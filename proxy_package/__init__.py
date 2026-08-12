import sys
import os

# 运行时路径。并非__init__.py的路径
BASE_DIR = "../awesome-backbones-main"

if os.path.exists(BASE_DIR):
    sys.path.append(BASE_DIR)
else:
    # 尝试下探一级路径
    sys.path.append("../../awesome-backbones-main")

# 导入项目的文件，请忽略静态错误

from configs import *
from core import *

from models import *
from tools import *
from utils import *