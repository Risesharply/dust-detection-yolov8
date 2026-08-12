# #Run inference on an image file.
#     #```python
from ultralytics import YOLO
import cv2
from ultralytics.utils import plotting
from ultralytics.utils import ops

    # Load a pretrained YOLOv8n model
model = YOLO('v8_weights/train9/best.pt')

    # Define path to the image file
source = '2.jpg'
frame = cv2.imread(source)
    # Run inference on the source
results=model(source)  # list of Results objects

print('___________________boxes.data_______________')
print(results[0].boxes.data)

print('___________________boxes_______________')
print(results[0].boxes)

print('___________________boxes.xyxy_______________')
print(results[0].boxes.xyxy)  #  xyxy 形式的目标框, (N, 4))

i=0
for box in results[0].boxes.xyxy:
    i=i+1
    ops.clip_boxes(box, frame)  # clip boxes
    cv2.imread(str(i)+'cut.img',box)

res= results[0].plot
cv2.imwrite('2_det.jpg',res)
print(results[0].boxes.cls)

#print(2 in results[0].boxes.cls)

# from collections import deque
#
# a= deque(maxlen=12)
# a.append(0)
# index = 1
# b = 0
# while True:
#     index += 1
#
#     ii=1
#     if index % 2 == 0:
#         b = b+2
#     else:
#         b=b+1
#     a.append(b)
#
#     c = sum(a)
#     if c > 4 :
#         print(a)
#         print('-------------------------')
