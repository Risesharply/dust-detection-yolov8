import os
import cv2


def txt_cut_image(image_path, txt_path, new_image_path,expand_size=300):
    # 遍历所有图片
    for file in os.listdir(image_path):
        image_file_path = os.path.join(image_path, file)

        # 构造对应的txt文件路径
        txt_file = os.path.splitext(file)[0] + ".txt"
        label_file_path = os.path.join(txt_path, txt_file)

        # 读取标注文件和原始图片
        with open(label_file_path, 'r') as f:
            lines = f.readlines()
        image = cv2.imread(image_file_path)

        # 循环处理每个标注框
        i = 0
        for line in lines:
            i = i + 1
            class_id, x_center, y_center, width, height = map(float, line.strip().split())

            if int(class_id)==2:

                # 将YOLOv5格式的坐标转换为常规坐标
                left = int((x_center - width / 2) * image.shape[1])
                top = int((y_center - height / 2) * image.shape[0])
                right = int((x_center + width / 2) * image.shape[1])
                bottom = int((y_center + height / 2) * image.shape[0])

                left = max(0, left - expand_size)
                top = max(0, top - expand_size)
                right = min(image.shape[1], right + expand_size)
                bottom = min(image.shape[0], bottom + expand_size)
                cut_image = image[top:bottom, left:right]

                # 如果剪切区域没有达到扩充的限制，才保存图片
                # if cut_image.shape[0] > expand_size * 2 and cut_image.shape[1] > expand_size * 2:
                #     cv2.imwrite(new_cut_image_path, cut_image)

                # 截取标注框内的内容并保存为新图片
                #cut_image = image[top:bottom, left:right]
                new_cut_image_path = os.path.join(new_image_path, file)
                print(new_cut_image_path)
                cv2.imwrite(new_cut_image_path, cut_image)

def labels_cut_image(image, labels, new_image_path,expand_size=100):
    # 遍历所有图片
    for file in os.listdir(image_path):
        image_file_path = os.path.join(image_path, file)

        # 构造对应的txt文件路径
        txt_file = os.path.splitext(file)[0] + ".txt"
        label_file_path = os.path.join(labels, txt_file)

        # 读取标注文件和原始图片
        with open(label_file_path, 'r') as f:
            lines = f.readlines()
        image = cv2.imread(image_file_path)

        # 循环处理每个标注框
        i = 0
        for line in lines:
            i = i + 1
            class_id, x_center, y_center, width, height = map(float, line.strip().split())

            if int(class_id)==2:

                # 将YOLOv5格式的坐标转换为常规坐标
                left = int((x_center - width / 2) * image.shape[1])
                top = int((y_center - height / 2) * image.shape[0])
                right = int((x_center + width / 2) * image.shape[1])
                bottom = int((y_center + height / 2) * image.shape[0])

                left = max(0, left - expand_size)
                top = max(0, top - expand_size)
                right = min(image.shape[1], right + expand_size)
                bottom = min(image.shape[0], bottom + expand_size)
                cut_image = image[top:bottom, left:right]

                # 如果剪切区域没有达到扩充的限制，才保存图片
                # if cut_image.shape[0] > expand_size * 2 and cut_image.shape[1] > expand_size * 2:
                #     cv2.imwrite(new_cut_image_path, cut_image)

                # 截取标注框内的内容并保存为新图片
                #cut_image = image[top:bottom, left:right]
                new_cut_image_path = os.path.join(new_image_path, file)
                print(new_cut_image_path)
                cv2.imwrite(new_cut_image_path, cut_image)
if __name__ == "__main__":
    image_path = "./data/images"
    txt_path = "./data/labels"
    new_image_path = "./data/new_images"
    txt_cut_image(image_path, txt_path, new_image_path)