
"""
TSYDD
"""
import torch
from .Tracker import Tracker

class NDS:
    def __init__(self, max_age=15, n_init=3):

        # tracker maintain a list contains(self.tracks) for each Track object
        self.tracker = Tracker(max_age=max_age, n_init=n_init)

    def refine_box(self, pred, update_class_id):
        # 输入：pred为该帧图像的检测结果,update_class_id为追踪的类别
        # 输出：refine_pred
        # 挑选dust_det
        dust_det = []
        dust_indices = []

        # 根据给定的类别标签选择目标信息进行运动轨迹跟踪
        for i, row in enumerate(pred):
            if row[-1] == update_class_id:
                dust_indices.append(i)
                dust_det.append(row[:4].tolist())

        # 使用GIoU_Tracker对选定的目标进行运动轨迹跟踪
        indices_to_remove = self.postProcessing(dust_det)
        indices = []
        # 根据跟踪结果选择需要删除的目标行的索引
        for i in indices_to_remove:
            indices.append(dust_indices[i])

        # 使用掩码张量删除指定索引的行
        mask = torch.ones(pred.size(0), dtype=torch.bool, device=pred.device)
        mask[indices] = False
        refine_pred = pred[mask]
        return refine_pred

    def postProcessing(self, detections):
        print('dets:', detections)
        # update tracker ********************************************************************************************
        self.tracker.predict()  # predict based on t-1 info

        # for first frame, this function do nothing

        # detections is the measurement results as time T
        remove_indices = self.tracker.update(detections)
        return remove_indices


    def clear_tracker(self):
        print('tracker clear')
        self.tracker.clear()



