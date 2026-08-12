
import numpy as np
tracks = []
sigma_work = 3
result = []
for track in tracks:

    if len(track.GIoUs) == 0:
        pass
    elif np.mean(track.GIoUs) > sigma_work:
        print(np.mean(track.GIoUs))
        print('*************')
        workState = 0
        result.append((track.track_id, workState))
    else:
        print(np.mean(track.GIoUs))
        print('_________________________')
        workState = 1
        result.append((track.track_id, workState))