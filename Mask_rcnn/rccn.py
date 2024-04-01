import os
import cv2
from pixellib.instance import instance_segmentation

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def object_detection_on_video(video_path):
    segment_video = instance_segmentation()
    segment_video.load_model("mask_rcnn_coco.h5")
    target_classes = segment_video.select_target_classes(person=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть видео.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: не удалось прочитать видео или видео закончилось.")
            break

        result = segment_video.segmentFrame(frame, segment_target_classes=target_classes, show_bboxes=True)

        frame_with_detections = result[1]

        cv2.imshow("Object Detections", frame_with_detections)

        # Нажмите 'q' для выхода из цикла
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    input_video_path = "file1.mp4"

    object_detection_on_video(input_video_path)


if __name__ == '__main__':
    main()
