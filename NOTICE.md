# Third-party notices

This research repository is based on [Ultralytics](https://github.com/ultralytics/ultralytics). The checked-out upstream version and its GNU AGPL v3 license are retained in `LICENSE` and the Git history.

The multi-object tracking logic in `methods/refine_tracking/` is adapted from ideas and implementation patterns in [bochinski/iou-tracker](https://github.com/bochinski/iou-tracker):

> MIT License - Copyright (c) 2017 TU Berlin, Communication Systems Group

The original MIT license permits use and modification provided that its copyright and permission notice are retained. This project modifies the tracker for dust detections, adds GIoU-based matching, track-state/time-series decisions, and YOLO detection-tensor filtering. The upstream iou-tracker repository is not vendored into this repository.

Please also cite the original IOU/V-IOU Tracker papers listed in the upstream repository when this tracking component is used in research.
