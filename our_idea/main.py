import cv2 as cv
import numpy as np
import requests

# img = cv.imread('0.JPG')
# img = cv.imread('1.JPG')
# img = cv.imread('2.JPG')
# img = cv.imread('3.JPG')
# img = cv.imread('4.JPG')
# img = cv.imread('5.JPG')

# img = cv.imread('0.JPG')

vid = cv.VideoCapture("ooo.mp4") # "football1.mp4" или 0/1 вместо названия файла, тогда откроется камера

prev_value = None

while(True): #vid.isOpened()  True
    ret, img = vid.read()
    img_size = [600, 1000]
    copy_img = img.copy()
    resized = cv.resize(copy_img, (img_size[1], img_size[0]))
    # frame = cv.resize(frame, (1000, 600)) #ужмем если видеофайл будет большого разрешения
    imgRoi = resized[50:50+300, 40:40+740]
    hsvMin = np.array((0, 0, 50), np.uint8)
    hsvMax = np.array((175, 40, 175), np.uint8)
    # bin = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    hsv1 = cv.cvtColor(imgRoi, cv.COLOR_BGR2HSV)
    binary = cv.inRange(hsv1, hsvMin, hsvMax)
    # copy_img1 = cv.blur(binary, (5, 5))
    # copyRoiErode = cv.erode(binary, (5, 5), iterations=3)
    # # cv.imshow("Erode", copyRoiErode)
    #
    # copyRoiErodeDilate = cv.dilate(copyRoiErode, (5, 5), iterations=6)
    number_of_black_pix = np.sum(binary == 0) # извлекаем только черные пиксели

    strelka = 0
    etolon = 9000
    onepeople = 19000
    Kolichestvo = (number_of_black_pix - etolon) // onepeople
    # strelka = Kolichestvo


    if Kolichestvo == 0:
        strelka = 0
    if Kolichestvo == 1:
        strelka = 1
    if Kolichestvo == 2:
        strelka = 2
    if Kolichestvo == 3:
        strelka = 3
    if Kolichestvo == 4:
        strelka = 4
    if Kolichestvo == 5:
        strelka = 5

    current_value = strelka
    if prev_value is not None and prev_value != current_value:

        url = 'http://доступный-град.рф/Convertor.php'
        data = {'data': strelka}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        timeout = 20

        response = requests.post(url, data=data, headers=headers, timeout=timeout)
        print(strelka)
    prev_value = current_value

    cv.imshow("binary", binary)
    # cv.imshow("original", img)

    # print(strelka)
    # print(number_of_black_pix)
    # print(response.text)    if ret is False:
    if ret is False:
        print("Камера не подключена")
        break

    cv.imshow('frame', imgRoi)


    if cv.waitKey(30) == 27:
        break
vid.release()
cv.destroyAllWindows()