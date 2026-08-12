

import torch
from proxy_package.utils.inference import inference_model, init_model
from proxy_package.utils.train_utils import get_info, file2dict
from models.build import BuildNet



class InferenceModel:
    def __init__(self, config='proxy_package/models/efficientnetv2/efficientnetv2_s.py',
                 classes_map='classify/annotations.txt', device='cuda'):
        self.classes_names, self.label_names = get_info(classes_map)

        # load the model
        model_cfg, train_pipeline, val_pipeline, data_cfg, lr_config, optimizer_cfg = file2dict(config)
        if device is not None:
            device = torch.device(device)
        else:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.model = BuildNet(model_cfg)
        self.model = init_model(self.model, data_cfg, device=device, mode='eval')
        self.val_pipeline = val_pipeline  # 将 'val_pipeline' 保存为属性，用于后续函数调用


    def classify_loader(self, img):
        t = 0
        result = inference_model(self.model, img, self.val_pipeline, self.classes_names,
                                 self.label_names)  # 调用 'self.val_pipeline'
        if result['pred_label'] == 0:
            t = 1

        return t
