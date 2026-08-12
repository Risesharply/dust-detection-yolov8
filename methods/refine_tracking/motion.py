

import torch
from .tracker import Tracker

class If_Move:
    def __init__(self, max_age=10, n_init=3):

        # tracker maintain a list contains(self.tracks) for each Track object
        self.tracker = Tracker(max_age=max_age, n_init=n_init)

    def get_workState(self, pred, update_class_id):
        # 输入：pred为该帧图像的检测结果,update_class_id为追踪的类别
        # 输出：refine_pred
        # 挑选dust_det
        loader_det = []
        loader_indices = []

        # 根据给定的类别标签选择目标信息进行运动轨迹跟踪
        for i, row in enumerate(pred):
            if row[-1] == update_class_id:
                loader_indices.append(i)
                loader_det.append(row[:4].tolist())

        # 使用GIoU_Tracker对loader进行运动轨迹更新
        # update tracker ********************************************************************************************
        self.tracker.predict()
        # 返回目前的轨迹数，及轨迹分类 作业or不作业 track_id, if_work
        result = self.tracker.M_update(loader_det)

        #返回当前loader轨迹分类 作业or不作业
        return result


    def clear_tracker(self):
        self.tracker.clear()


