import cv2 as cv
import numpy as np

# cap = cv.VideoCapture("0401(1).mp4")

try:
    cap = cv.VideoCapture("0401.mp4")
except cv.error as e:
    print("OpenCV VideoCapture error:", e)
    exit()
try:
    hsvMin = np.array((0, 0, 95), np.uint8)
    hsvMax = np.array((185, 50, 255), np.uint8)

    while True:

        ret, img = cap.read()
        img_size = [600, 600]
        copy_img = img.copy()
        resized = cv.resize(copy_img, (img_size[1], img_size[0]))

        hsv1 = cv.cvtColor(resized, cv.COLOR_BGR2HSV)
        copy_img = cv.inRange(hsv1, hsvMin, hsvMax)
        imgRoi1 = copy_img[160:160 + 150, 160:160 + 50]
        imgRoi2 = copy_img[95:95 + 170, 410:410 + 30]

        # Получение высоты и ширины изображения
        height, width = imgRoi1.shape
        flag1 = False
        kolichestvo_edi_1 = 0

        # Перебор каждой строки изображения (y)
        for y in range(height):
            black_pixels = sum(1 for x in range(width) if imgRoi1[y, x] == 0)  # Подсчет черных пикселей
            white_pixels = sum(1 for x in range(width) if imgRoi1[y, x] == 255)  # Подсчет белых пикселей
            if black_pixels > white_pixels and flag1 == False:
                kolichestvo_edi_1 = round(((height-y)/height)*100)
                print(y)
                flag1 = True

        # Получение высоты и ширины изображения
        height, width = imgRoi2.shape
        flag2 = False
        kolichestvo_edi_2 = 0

        # Перебор каждой строки изображения (y)
        for y in range(height):
            black_pixels = sum(1 for x in range(width) if imgRoi2[y, x] == 0)  # Подсчет черных пикселей
            white_pixels = sum(1 for x in range(width) if imgRoi2[y, x] == 255)  # Подсчет белых пикселей
            if black_pixels > white_pixels and flag2 == False:
                kolichestvo_edi_2 = round(((height-y)/height)*100)
                print(y)
                flag2 = True

        cv.imshow("Original", resized)
        cv.imshow("HSV", copy_img)
        cv.imshow("ROI1", imgRoi1)
        cv.imshow("ROI2", imgRoi2)
        # if kolichestvo_edi_1 and kolichestvo_edi_2 != 0:
        print('количесвто жёлтой еды =' , kolichestvo_edi_1,'%')
        print('количесвто красной еды =' , kolichestvo_edi_2,'%')

        if cv.waitKey(30) == 27:
            break

except Exception as e:
    print("An error occurred:", e)
# vid.release()
# cv.destroyAllWindows()
finally:
    try:
        # ser.close()
        vid.release()
        cv.destroyAllWindows()
    except NameError:
        pass

