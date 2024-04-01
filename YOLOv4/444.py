import sys

# Путь к вашей библиотеке
library_path = r"C:\Users\общий\Desktop\YOLOv4\darknet"

# Добавляем путь к библиотеке в PYTHONPATH
sys.path.insert(0, library_path)

# Импортируем вашу библиотеку
# from darknet import darknet
import darknet
# import sys
# sys.path.append(r'C:\Users\общий\Desktop\YOLOv4\darknet\darknet.py')
# import darknet
# from darknet import darknet
import cv2
import numpy as np

net = darknet.load_network(r"C:\Users\общий\Desktop\YOLOv4\darknet\build\darknet\x64\cfg\yolov4.cfg", r"C:\Users\общий\Desktop\YOLOv4\darknet\build\darknet\x64\yolov4.weights", 0)
meta = darknet.load_meta(r"C:\Users\общий\Desktop\YOLOv4\darknet\build\darknet\x64\data\coco.data")

cap = cv2.VideoCapture("file1.mp4")
ret, frame = cap.read()
frame_counter = 0
frame_interval = 5

while ret:
    frame_counter += 1
    if frame_counter % frame_interval == 0:
        frame_resized = cv2.resize(frame, (darknet.network_width(net), darknet.network_height(net)))
        darknet_image = darknet.make_image(darknet.network_width(net), darknet.network_height(net), 3)

        darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())

        detections = darknet.detect_image(net, meta, darknet_image)

        for detection in detections:
            label = detection[0]
            confidence = detection[1]
            x, y, w, h = detection[2]

            # cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2), (0, 255, 0), 1)
            cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 1)
            cv2.putText(frame, label, (int(x - w / 2), int(y - h / 2 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            cv2.imshow("Object Detection", frame)

            darknet.free_image(darknet_image)

            ret, frame = cap.read()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()