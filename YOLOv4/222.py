import cv2
import numpy as np

# Load YOLOv4 weights and configuration file
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i [0] - 1] for i in net.getUnconnectedOutLayers()]

# Определение индексов выходных слоев
layer_names = net.getLayerNames()
# layer_ids = net.getUnconnectedOutLayers()
# output_layers = [layer_names[i[0] - 1] for i in layer_ids]


layer_ids = net.getUnconnectedOutLayers()
print("layer_ids:", layer_ids)
# output_layers = [layer_names[i[0] - 1] for i in layer_ids]
output_layers = [layer_names[layer_id - 1] for layer_id in layer_ids]
print("output_layers:", output_layers)

# Load COCO class labels
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f]

# Read video file
video = cv2.VideoCapture("file1.mp4")

while True:
    ret, frame = video.read()
    if not ret:
        break

    # YOLOv4 Object Detection
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Post-processing
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Object detected
                box = detection[0:4] * np.array([416, 416, 416, 416])
                (x, y, w, h) = box.astype("int")
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, classes[class_id], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display output
    cv2.imshow("YOLOv4 Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()