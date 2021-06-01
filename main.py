# 패키지 설치
# pip install dlib opencv-python
#
# 학습 모델 다운로드
# http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import dlib
import cv2 as cv
import numpy as np
import math

def alert_chin():
    tkinter.messagebox.showinfo("Alert", "고개 돌리지 마세요.")
    now = datetime.now()
    print("%s년 %s월 %s일 %s시 %s분 %s초.%s 고개 돌림 감지" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))

window = Tk()
detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

cap = cv.VideoCapture(0)

# range는 끝값이 포함안됨
ALL = list(range(0, 68))
RIGHT_EYEBROW = list(range(17, 22))
LEFT_EYEBROW = list(range(22, 27))
RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
NOSE = list(range(27, 36))
MOUTH_OUTLINE = list(range(48, 61))
MOUTH_INNER = list(range(61, 68))
JAWLINE = list(range(0, 17))

index = ALL

while True:

    ret, img_frame = cap.read()

    img_gray = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)

    dets = detector(img_gray, 1)

    for face in dets:

        shape = predictor(img_frame, face)  # 얼굴에서 68개 점 찾기

        list_points = []
        for p in shape.parts():
            list_points.append([p.x, p.y])
            #print(list_points)

        list_points = np.array(list_points)
        num = 0
        left_eye_x = 0
        left_eye_y = 0
        right_eye_x = 0
        right_eye_y = 0
        for i, pt in enumerate(list_points[index]):
            pt_pos = (pt[0], pt[1])
            if num == 29:
                nose_x = pt_pos[0]
                nose_y = pt_pos[1]
                #print("코코코 레드코~~" , nose_x, " ", nose_y)
            if num == 37 or num == 40:
                left_eye_x = left_eye_x + pt_pos[0]
                left_eye_y = left_eye_y + pt_pos[1]
            if num == 41:
                left_eye_x = left_eye_x // 2
                left_eye_y = left_eye_y // 2
                #print("눈눈눈 왼쪽눈~~", left_eye_x, " ", left_eye_y)
            if num == 44 or num == 47:
                right_eye_x = right_eye_x + pt_pos[0]
                right_eye_y = right_eye_y + pt_pos[1]
            if num == 48 :
                right_eye_x = right_eye_x // 2
                right_eye_y = right_eye_y // 2
                #print("눈눈눈 오른눈~~", right_eye_x, " ", right_eye_y)
            cv.circle(img_frame, pt_pos, 2, (0, 255, 0), -1)
            num=num+1

        cv.rectangle(img_frame, (face.left(), face.top()), (face.right(), face.bottom()),
                     (0, 0, 255), 3)
        nose_to_eye_left_x = nose_x - left_eye_x
        nose_to_eye_left_y = nose_y - left_eye_y
        nose_to_eye_right_x = nose_x - right_eye_x
        nose_to_eye_right_y = nose_y - right_eye_y
        norm_left = math.sqrt(nose_to_eye_left_x**2 + nose_to_eye_left_y**2)
        norm_right = math.sqrt(nose_to_eye_right_x ** 2 + nose_to_eye_right_y ** 2)
        #print(norm_left, " ",norm_right)
        if abs(norm_left - norm_right) >= 20:
            alert_chin()


    cv.imshow('result', img_frame)

    key = cv.waitKey(1)

    if key == 27:
        break

    elif key == ord('1'):
        index = ALL
    elif key == ord('2'):
        index = LEFT_EYEBROW + RIGHT_EYEBROW
    elif key == ord('3'):
        index = LEFT_EYE + RIGHT_EYE
    elif key == ord('4'):
        index = NOSE
    elif key == ord('5'):
        index = MOUTH_OUTLINE + MOUTH_INNER
    elif key == ord('6'):
        index = JAWLINE

cap.release()

