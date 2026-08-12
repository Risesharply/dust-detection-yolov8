import numpy as np

from .track import *
from .matching import *
'''
Tracker类
属性
    max_age:一个跟踪对象丢失多少帧后会被删去
    n_init:连续n_init帧被检测到，状态就被设为confirmed
    giou_distance：在做IOU匹配的时候用到的阈值

    _next_id:记录下一个跟踪对象的id号
    tracks：保存跟踪对象的列表
方法：
    核心是IoU匹配，
    predict：对所有跟踪对象进行坐标预测
    update：特征匹配，更新所有跟踪对象的状态。
    giou_match: 进行GIoU匹配
    _initiate_track：初始化一个新的跟踪对象

'''
class Tracker:
    def __init__(self, max_age=20, n_init=4):

        self.max_age = max_age
        self.n_init = n_init

        self.tracks = []
        self._next_id = 1
        self.sigma_giou = -0.2
        self.reference = []
        self.sigma_error = 0.7
        self.sigma_work = 0.86

    def predict(self):
        # STEP 1: at each time T, firstly we predict x' of each Track obj with tracks' lastest bboxes
        """
        Propagate track state distributions one time step forward.
        This function should be called once every time step, before `update`.
        """
        self.reference = []

        for track in self.tracks:
            # for each obj,  provide reference bbox  based on t-1  为空列表或refer bbox
            print("track_id:",track.track_id )
            print("track_GIoUs:",track.GIoUs)
            print('------------------------------')
            print("len:",len(track.GIoUs))
            refer = track.predict()
            self.reference.append(refer)
        print('refer:', self.reference)



    def update(self, detections):
        # STEP 2: Then we update
        """Perform measurement update and track management.

        Parameters
        ----------
        detections : List[deep_sort.detection.Detection]
            A list of detections at the current time step.
            each Detection obj maintain the location(bbox_tlwh)
        """
        # IOU matching *************************************************************************************
        #matches=[(1,3,giou),..] 其他是[1,3,4,..]
        length = len(detections)
        det_error = [0]*length

        matches, unmatched_tracks, unmatched_detections = giou_matching(self.reference, detections, self.sigma_giou)
        print('match:',matches)
        print('unmatch:', unmatched_tracks)
        print('unmatch_det:',unmatched_detections )
        # Update track set.
        #匹配成功，添加det到track.location
        if matches != []:
            for index_t,index_d, giou in matches:
                self.tracks[index_t].update(detections[index_d], giou)
                det_error[index_d] = np.mean(self.tracks[index_t].GIoUs)

        for index_d in unmatched_detections:

            self._initiate_track(detections[index_d])
            det_error[index_d] = 0

        for index_t in unmatched_tracks:
            self.tracks[index_t].mark_missed()

        self.tracks = [t for t in self.tracks if not t.is_deleted()]

        print('error:',det_error)
        remove_indices = self.filter_detections(det_error,self.sigma_error)
        return remove_indices

    def M_update(self, detections):

        key_frame = 0
        #matches=[(1,3,giou),..] 其他是[1,3,4,..]
        matches, unmatched_tracks, unmatched_detections = giou_matching(self.reference, detections, self.sigma_giou)
        print('match:',matches)
        print('unmatch:', unmatched_tracks)
        print('unmatch_det:',unmatched_detections )
        # Update track set.
        #匹配成功，添加det到track.location
        if matches != []:
            for index_t,index_d, giou in matches:
                self.tracks[index_t].update(detections[index_d], giou)
                if giou > 0.97:
                    self.tracks[index_t].key_frame = 1

        for index_d in unmatched_detections:
            self._initiate_track(detections[index_d])

        for index_t in unmatched_tracks:
            self.tracks[index_t].mark_missed()

        self.tracks = [t for t in self.tracks if not t.is_deleted()]

        #对轨迹是否作业进行分类
            #初始化 轨迹列表 作业状态列表
        result=[]
        key = 0
        for track in self.tracks:

            if len(track.GIoUs) == 0:
                pass
            elif np.mean(track.GIoUs) > self.sigma_work:
                    print(np.mean(track.GIoUs))
                    print('*************')
                    workState = 0
                    result.append((track.track_id, workState,key))
            else:
                print(np.mean(track.GIoUs))
                print('_________________________')
                workState = 1
                if track.key_frame == 1:
                    key = 1
                track.key_frame = 0
                result.append((track.track_id, workState,key))

        #返回轨迹id 轨迹作业情况
        print('result:',result)

        return result

    def _initiate_track(self, detection):
        #该unmatched detection信息为初始信息
        self.tracks.append(Track(self._next_id, self.n_init, self.max_age,detection)) # for new obj, create a new Track object for it
        self._next_id += 1


    def filter_detections(self, list_error, sigma_error):
        remove_indices = []
        for i, error in enumerate(list_error):
            if error > sigma_error:
                remove_indices.append(i)
        return remove_indices

    def clear(self):
        self.tracks = []
        self._next_id = 1


