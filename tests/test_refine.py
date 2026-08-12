import math

import torch

from methods.refine_tracking import NDS
from methods.refine_tracking.matching import GIoU, iou
from methods.refine_tracking.tracker import Tracker


def test_iou_for_identical_and_disjoint_boxes():
    assert iou([0, 0, 10, 10], [0, 0, 10, 10]) == 1.0
    assert iou([0, 0, 1, 1], [2, 2, 3, 3]) == 0.0


def test_degenerate_boxes_are_finite():
    assert math.isfinite(iou([0, 0, 0, 0], [0, 0, 0, 0]))
    assert math.isfinite(GIoU([0, 0, 0, 0], [0, 0, 0, 0]))


def test_tracker_creates_and_clears_tracks():
    tracker = Tracker(max_age=2, n_init=1)
    tracker.predict()
    assert tracker.update([[0, 0, 10, 10]]) == []
    assert len(tracker.tracks) == 1
    tracker.clear()
    assert tracker.tracks == []
    assert tracker._next_id == 1


def test_nds_preserves_non_target_rows_on_first_frame():
    detections = torch.tensor([[0, 0, 10, 10, 0.9, 0], [1, 1, 5, 5, 0.8, 1]])
    refined = NDS().refine_box(detections, update_class_id=0)
    assert torch.equal(refined, detections)
