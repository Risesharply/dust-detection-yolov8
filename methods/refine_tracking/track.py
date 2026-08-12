
'''
属性：
    location: 存储track的轨迹信息，即bbox
    track_id：跟踪对象的id号
    hits：就是该对象已经进行了多少次预测了，也就是predict()
    age：第一次出现到现在一共多少帧
    time_since_update ：上一次更新距离现在多少帧，在匹配上之后会置为0
    ttl:视觉跟踪
    GIoU: 用来计算error 当匹配成功，track增加时GIoU序列加1
    state：该跟踪对象的状态
        Tentative：检测到新目标的时候状态设为Tentative，当其匹配上的次数不超过_n_init时都是该状态
        Confirmed：当匹配上的次数超过_n_init且未匹配上的次数小于max_age时
        Deleted：未匹配上（也就是距离上一次更新）的次数超过max_age，或者处于Tentative时的跟踪对象未匹配上就直接变成Deleted
**************************************
Track状态转换的方法及条件：
    max_age:一个跟踪对象丢失多少帧后会被删去,
    n_init:连续n_init帧被检测到，状态就被设为confirmed
**************************************
方法：
    to_tlwh:
    to_tlbr:这两个方法都是改变bbox坐标格式
    predict：对该跟踪对象进行坐标预测
    update：对该跟踪对象进行坐标更新
    mark_missed：把跟踪对象状态标记为Deleted
    is_tentative：把跟踪对象状态标记为Tentative
    is_confirmed：把跟踪对象状态标记为Confirmed
    is_deleted：把跟踪对象状态标记为Deleted
'''

class TrackState:
    """
    Enumeration type for the single target track state. Newly created tracks are
    classified as `tentative` until enough evidence has been collected. Then,
    the track state is changed to `confirmed`. Tracks that are no longer alive
    are classified as `deleted` to mark them for removal from the set of active
    tracks.

    """

    Tentative = 1
    Confirmed = 2
    Deleted = 3

class Track:

    def __init__(self,track_id, n_init, max_age,location):
        self.location = [location]
        self.track_id = track_id
        self.hits = 1
        self.age = 1
        self.time_since_update = 0
        self.ttl = 5

        self.state = TrackState.Tentative
        self._n_init = n_init
        self._max_age = max_age
        self.GIoUs = []
        self.key_frame = 0

    def predict(self):

        """ Predict the next location of the tracked object using last known location.

        Args:
            ttl (int, optional): time-to-live. The maximum number of frames the tracker can remain undetected
                                 before it's destroyed. Default: 5
        Returns:
            A tuple of (bool, tuple): if the prediction is successful, return True and the predicted location
            (x1, y1, w, h). Otherwise, return False and None.
        """
        #refer = []
        self.age += 1
        self.time_since_update += 1
        refer = self.location[-1]
        # for i in range(-1, -self.ttl - 1, -1):  # loop over last ttl positions of the tracked object
        #     if i < -len(self.location):  # no location history available
        #         break
        #
        #     refer = self.location[i]

        return refer  # no valid location found in the last ttl positions



    def update(self,detection,giou):

        self.location.append(detection)
        self.GIoUs.append(giou)
        self.hits += 1
        self.time_since_update = 0
        if self.state == TrackState.Tentative and self.hits >= self._n_init:
            self.state = TrackState.Confirmed


    def mark_missed(self):
        """Mark this track as missed (no association at the current time step).
        """
        if self.state == TrackState.Tentative:
            self.state = TrackState.Deleted
        elif self.time_since_update > self._max_age:
            self.state = TrackState.Deleted

    def is_tentative(self):
        """Returns True if this track is tentative (unconfirmed).
        """
        return self.state == TrackState.Tentative

    def is_confirmed(self):
        """Returns True if this track is confirmed."""
        return self.state == TrackState.Confirmed

    def is_deleted(self):
        """Returns True if this track is dead and should be deleted."""
        return self.state == TrackState.Deleted

