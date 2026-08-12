import cv2
import torch
from ultralytics import YOLO
from refine.TSYDD import NDS
#from refine.PPMove import If_Move
from proxy_package.root_test import classify_loader

'''

class ThreadedCamera(object):
    def __init__(self, source=0):

        self.source = source
        self.capture = cv2.VideoCapture(self.source)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True  # 防止主线程挂掉，子线变成程僵尸进程
        self.thread.start()

        self.status = False
        self.frame = None

        self.n_frames = 0
        self.skip_frames = 6

        self.aa = " "

    def update(self):
        while True:
            if self.capture.isOpened():
                self.capture.grab()
                self.n_frames += 1
                if self.n_frames % self.skip_frames != 0:
                    continue
                self.status, self.frame = self.capture.retrieve()
                self.aa = "t1=" + time.strftime("%Y-%m-%d %H:%M:%S")
            if not self.status:
                with open(f'errorlog.txt', 'a') as f:
                    f.writelines(self.aa + '--' + self.source + '_Error')
                print("等待10s后重连")
                time.sleep(5)
                self.capture = cv2.VideoCapture(self.source)
                print('restart success!!')

    def grab_frame(self):
        if self.status:
            return self.frame
        return None


# 单独的线程类，用于处理摄像头流
class AlogrithmThread(threading.Thread):
    # model = None  # 类变

    def __init__(self, camera_id, stream_link):
        super(AlogrithmThread, self).__init__()
        self.streamer = ThreadedCamera(stream_link)
        self.camera_id = camera_id
        self.index = 0
        self.i = 0
        self.skip_frame = 8
        self.post_process = NDS()
        self.If_work = If_Move()
        self.model = YOLO('v8_weights/6class_bu27img/best.pt', task='detect')
        img = np.zeros((480, 640, 3), np.uint8)
        img_rgb = img.copy()
        img_rgb[:, :, :] = [255, 255, 255]
        self.img = [img_rgb for i in range(10)]
        self.new_pattern_points_list = []


    def run(self):
        while True:
            self.index += 1
            time.sleep(0.1)

            frame = self.streamer.grab_frame()
            if frame is not None:
                # yolov8处理
                try:
                    with torch.no_grad():
                        results = self.model(frame)

                except Exception as e:
                    print(str(e))
                    print('error\n')

                # 后处理方法
                results[0].boxes.data = self.post_process.refine_box(results[0].boxes.data,
                                                                     0)  # tensor([[324.90079, 167.98221, 387.97580, 229.84625,   0.57933,   0.00000]], device='cuda:0')
                w_results= self.If_work.get_workState(results[0].boxes.data,
                                                                     2)  # tensor([[324.90079, 167.98221, 387.97580, 229.84625,   0.57933,   0.00000]], device='cuda:0')

                frame = results[0].plot()
                Nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, Nowtime, (1720, 1760), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 3)

                if w_results!= None:
                    for i in range(len(w_results)):
                        cv2.putText(frame, str(w_results[i]), (100, 100+50*i), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 3)
                frame = cv2.resize(frame, (640, 480))
                # 保存结果
                cv2.imwrite('imgs/det'+str(self.index)+'.jpg',frame)


if __name__ == '__main__':
    # 183-28-0,188-5-1,190-25-2,192-3-3,194-4-4,196-27-5,198-29-6,

    # 多个ThreadedCamera对象
    # 创建多个线程，并启动它们
    stream_links = ["rtsp://127.0.0.1:554/live/test"]
    # "rtsp://10.128.247.190/11","rtsp://10.128.247.192/11",
    # "rtsp://10.128.247.194/11","rtsp://10.128.247.196/11","rtsp://10.128.247.198/11"]
    # 开始处理每个源的图片
    threads = [AlogrithmThread(index, link) for index, link in enumerate(stream_links)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
'''


# 处理单个视频
cap = cv2.VideoCapture('D:/FFOutput/13.mp4')  # 0
#cap = cv2.VideoCapture('D:/video/stain_7_21_5.mp4')  # 0
model = YOLO('v8_train5/best.pt', task='detect')
post_process = NDS()
#If_work = If_Move()
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 视频编解码器
fps = cap.get(cv2.CAP_PROP_FPS)  # 帧数
width, height = 640, 480 # 宽高
out = cv2.VideoWriter('E:/images/mot_work1/13.mp4', fourcc, fps, (width, height))  # 写入视频
#out = cv2.VideoWriter('D:/video/paper/5_det.mp4', fourcc, fps, (width, height))  # 写入视频

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
                temp_data = results[0].boxes.data
                results[0].boxes.data = post_process.refine_box(temp_data,0)  # tensor([[324.90079, 167.98221, 387.97580, 229.84625,   0.57933,   0.00000]], device='cuda:0')
                #w_results= If_work.get_workState(temp_data,2)  # tensor([[324.90079, 167.98221, 387.97580, 229.84625,   0.57933,   0.00000]], device='cuda:0')


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
                # cv2.imshow("video", img)
            if not rec:
                break  # 当获取完最后一帧就结束

    # 释放资源
    cap.release()
    out.release()
    # 关闭窗口
    cv2.destroyAllWindows()



