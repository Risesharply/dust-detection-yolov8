import cv2
import torch
from ultralytics import YOLO
from refine.TSYDD import NDS
#from refine.PPMove import If_Move
from proxy_package.root_test import classify_loader


# 处理单个视频
cap = cv2.VideoCapture('D:/FFOutput/P20231218_235412_235959.mp4')  # 0
#cap = cv2.VideoCapture('D:/video/stain_7_21_5.mp4')  # 0
model = YOLO('v8_train5/best.pt', task='detect')
#post_process = NDS()
#If_work = If_Move()
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 视频编解码器
fps = cap.get(cv2.CAP_PROP_FPS)  # 帧数
width, height = 640, 480 # 宽高
#out = cv2.VideoWriter('E:/images/mot_work1/1.mp4', fourcc, fps, (width, height))  # 写入视频
out = cv2.VideoWriter('E:/images/video/12_19_1.mp4', fourcc, fps, (width, height))  # 写入视频

if __name__ == '__main__':
    with torch.no_grad():
        j=0
        while True:
            rec, frame = cap.read()

            if rec == True:
                # yolov8处理
                try:
                    with torch.no_grad():
                        results = model(frame)

                except Exception as e:
                    print(str(e))
                    print('error\n')
                # 后处理方法
                #temp_data = results[0].boxes.data
                #results[0].boxes.data = post_process.refine_box(temp_data,0)  # tensor([[324.90079, 167.98221, 387.97580, 229.84625,   0.57933,   0.00000]], device='cuda:0')
                #w_results= If_work.get_workState(temp_data,2)  # tensor([[324.90079, 167.98221, 387.97580, 229.84625,   0.57933,   0.00000]], device='cuda:0')

                boxes = results[0].boxes.data

                h = frame.shape[0]
                w = frame.shape[1]

                THRESH = 20  # 阈值


                # def filter_boxes(boxes, img_shape):
                #     """
                #     筛选未靠近四周边缘的 box
                #     :param boxes: 检测到的 box 列表 [(x1,y1,x2,y2), ...]
                #     :param img_shape: 图像的大小 (h,w)
                #     :return: 未靠近四周边缘的 box 列表 [(x1,y1,x2,y2), ...]
                #     """
                #     filtered_boxes = []  # 过滤后的 box
                #     h, w = img_shape[:2]
                #
                #     for box in boxes:
                #         x, y1, x2, y2 = box
                #         # 判断 box 是否靠近四边缘
                #         if x1 < THRESHOLD or y1 < THRESHOLD or w - x2 < THRESHOLD or h - y2 < THRESHOLD            continue  # 靠近四周边缘
                #         else:
                #             filtered_boxes.append(box)  # 未靠近四周边缘
                #
                #     return filtered_boxes


                #if loader exists,crop loader object to classify network

                loader_boxes = []

                if boxes != None:
                    i = 0
                    for box in boxes:

                        class_id = box[5]
                        left = box[0].int()
                        top = box[1].int()
                        right = box[2].int()
                        bottom =box[3].int()

                        center_x = (left+right)/2.0
                        center_y = (top+bottom)/2.0

                        expand_size = int((right-left)/8)
                        if int(class_id) == 2:
                            j=j+1
                            # 将YOLOv8格式的坐标转换为常规坐标
                            left = max(0, left - expand_size)
                            top = max(0, top - expand_size)
                            right = min(w, right + expand_size)
                            bottom = min(h, bottom + expand_size)
                            cut_image = frame[top:bottom, left:right]

                            classify_result= classify_loader(cut_image)

                             #if classified result is down,print "down","xywh"

                            if classify_result:
                                i = i + 1
                                loader_boxes.append((i,[center_x.__float__(),center_y.__float__()]))
                    if loader_boxes != None:
                        for i in range(len(loader_boxes)):
                            spray_work = 'dust'+',site:'+str(loader_boxes[i][1])
                            cv2.putText(frame, spray_work, (50, 200 + 200 * i), cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 255), 5)


                #Nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
                #cv2.putText(frame, Nowtime, (1080, 920), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 2)
                '''
                count =0
                if w_results!= None:
                    for i in range(len(w_results)):
                        #查看当前所有轨迹状态
                        state = w_results[i][1]
                        if state == 0 :
                            workstate='not'
                        else:
                            workstate='work'
                        if w_results[i][2] ==1 :
                            key = 'Key'
                        else:
                            key = ''

                        loader_work='Track'+str(i+1)+':'+workstate +' '+key
                        cv2.putText(frame, loader_work, (50, 70+70*i), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                            '''
                frame = results[0].plot()
                frame = cv2.resize(frame, (640, 480))
                out.write(frame)
                #cv2.imshow("video", img)
            if not rec:
                break  # 当获取完最后一帧就结束

    # 释放资源
    cap.release()
    #out.release()
    # 关闭窗口
    cv2.destroyAllWindows()



