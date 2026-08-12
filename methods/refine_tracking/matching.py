import numpy as np


def iou(box1, box2):
    # detection为xyxy格式
    # 计算中间矩形的宽高
    in_w = min(box1[2], box2[2]) - max(box1[0], box2[0])
    in_h = min(box1[3], box2[3]) - max(box1[1], box2[1])

    # 计算交集、并集面积
    inter = 0 if in_w <= 0 or in_h <= 0 else in_h * in_w

    union = (box2[2] - box2[0]) * (box2[3] - box2[1]) + \
            (box1[2] - box1[0]) * (box1[3] - box1[1]) - inter

    # 计算IoU
    return inter / union if union > 0 else 0.0


def GIoU(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2
    area_c = (max(x2, x4) - min(x1, x3)) * \
             (max(y4, y2) - min(y3, y1))
    # 计算中间矩形的宽高
    in_w = min(box1[2], box2[2]) - max(box1[0], box2[0])
    in_h = min(box1[3], box2[3]) - max(box1[1], box2[1])

    # 计算交集、并集面积
    inter = 0 if in_w <= 0 or in_h <= 0 else in_h * in_w

    union = (box2[2] - box2[0]) * (box2[3] - box2[1]) + \
            (box1[2] - box1[0]) * (box1[3] - box1[1]) - inter

    # 计算IoU
    iou = inter / union if union > 0 else 0.0
    # 计算空白面积
    blank_area = area_c - union
    # 计算空白部分占比
    blank_count = blank_area / area_c if area_c > 0 else 0.0
    giou = iou - blank_count

    return giou



def giou_matching(track_boxes, detection_boxes, giou_threshold):
    """
        Match detection boxes with track boxes based on GIoU.

    detections : List[detection.Detection]
        A list of detections at the current time step.
    track_indices : List[int]
        List of track indices that maps rows in `cost_matrix` to tracks in
        `tracks` (see description above).
    detection_indices : List[int]
        List of detection indices that maps columns in `cost_matrix` to
        detections in `detections` (see description above).
    Returns
    -------
    (List[(int, int)], List[int], List[int])
        Returns a tuple with the following three entries:
        * A list of matched track and detection indices.
        * A list of unmatched track indices.
        * A list of unmatched detection indices.
    """
    len_t = len(track_boxes)
    len_d = len(detection_boxes)
    track_indices = np.arange(len_t)
    detection_indices =np.arange(len_d)

    #giou matrix calculated
    giou_matrix = np.zeros((len_t, len_d), dtype=float)

    matches, unmatched_tracks, unmatched_detections = [], [], []

    for i, track_box in enumerate(track_boxes):
        for j , det in enumerate(detection_boxes):
            if track_box and det:
                giou_matrix[i,j] = GIoU(track_box,det)
            else:
                giou_matrix[i,j] = -1
    # match
    #step1.确定matches
    # 找到每列的最大值及其索引
    a = np.array(giou_matrix)

    rows, cols = [], []
    if a.size == 0:
        matches=[]
    else:
        max_values = np.max(giou_matrix, axis=0)
        max_indices = np.argmax(giou_matrix, axis=0)
        # 找到大于0.4的最大值的索引
        indices = np.where(max_values > giou_threshold)

        for index in indices[0]:
            row = max_indices[index]
            col = index
            rows.append(row)
            cols.append(col)
            matches.append((row, col, giou_matrix[row,col]))

    row_indices = np.array(rows)
    col_indices = np.array(cols)

    #step2.确定unmatched_detections
    for col, detection_idx in enumerate(detection_indices):
        if col not in col_indices:
            unmatched_detections.append(detection_idx)
    #step3确定unmatched_tracks，matches里row中没有的
    for row, track_idx in enumerate(track_indices):
        if row not in row_indices:
            unmatched_tracks.append(track_idx)

    return matches, unmatched_tracks, unmatched_detections
'''
def v_giou_matching(track_boxes, detection_boxes, giou_threshold):
    """
        Match detection boxes with track boxes based on GIoU.

    detections : List[detection.Detection]
        A list of detections at the current time step.
    track_indices : List[int]
        List of track indices that maps rows in `cost_matrix` to tracks in
        `tracks` (see description above).
    detection_indices : List[int]
        List of detection indices that maps columns in `cost_matrix` to
        detections in `detections` (see description above).
    Returns
    -------
    (List[(int, int)], List[int], List[int])
        Returns a tuple with the following three entries:
        * A list of matched track and detection indices.
        * A list of unmatched track indices.
        * A list of unmatched detection indices.
    """
    len_t = len(track_boxes)
    len_d = len(detection_boxes)
    track_indices = np.arange(len_t)
    detection_indices =np.arange(len_d)

    #giou matrix calculated
    giou_matrix = np.zeros((len_t, len_d), dtype=float)

    matches, unmatched_tracks, unmatched_detections = [], [], []

    for i, track_box in enumerate(track_boxes):
        for j , det in enumerate(detection_boxes):
            if track_box and det:
                giou_matrix[i,j] = GIoU(track_box,det)
            else:
                giou_matrix[i,j] = -1
    # match
    #step1.确定matches
    # 找到每列的最大值及其索引
    a = np.array(giou_matrix)

    rows, cols = [], []
    if a.size == 0:
        matches=[]
    else:
        max_values = np.max(giou_matrix, axis=0)
        max_indices = np.argmax(giou_matrix, axis=0)
        # 找到大于0.4的最大值的索引
        indices = np.where(max_values > giou_threshold)

        for index in indices[0]:
            row = max_indices[index]
            col = index
            rows.append(row)
            cols.append(col)
            matches.append((row, col))

    row_indices = np.array(rows)
    col_indices = np.array(cols)

    #step2.确定unmatched_detections
    for col, detection_idx in enumerate(detection_indices):
        if col not in col_indices:
            unmatched_detections.append(detection_idx)
    #step3确定unmatched_tracks，matches里row中没有的
    for row, track_idx in enumerate(track_indices):
        if row not in row_indices:
            unmatched_tracks.append(track_idx)

    return matches, unmatched_tracks, unmatched_detections
'''
