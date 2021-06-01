"""
https://github.com/antoinelame/GazeTracking
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import dlib
import numpy as np
import cv2
from gaze_tracking import GazeTracking  # 눈동자 추적 library

import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

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

eye_r_count = 0
eye_l_count = 0

def alert(str):
    tkinter.messagebox.showinfo("Alert", str)
    now = datetime.now()
    print("%s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    eye_r_count = 0
    eye_l_count = 0

window = Tk()


while True:
    # 웹캠 불러옴
    ret, frame = webcam.read()
    text = ""

    # gazeTracking에서 frame분석 후 저장
    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    # 분석된 gaze frame 바탕으로 눈동자 방향 분석 후 출력
    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "right"
        eye_r_count = eye_r_count + 1
        if eye_r_count >= 5: # 5 frame 이상 쳐다보면
            alert("right")
    elif gaze.is_left():
        text = "left"
        eye_l_count = eye_l_count + 1
        if eye_l_count >= 5:
            alert("left")
    elif gaze.is_center():
        text = "center"
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    # 눈동자 위치 출력
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # 수아꺼
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dets = detector(img_gray, 1)

    for face in dets:
        shape = predictor(frame, face)  # 얼굴에서 68개 점 찾기
        list_points = []
        for p in shape.parts():
            list_points.append([p.x, p.y])
        list_points = np.array(list_points)
        num = 0

        for i, pt in enumerate(list_points[index]):
            pt_pos = (pt[0], pt[1])
            if num == 29:
                nose_x = pt_pos[0]
                nose_y = pt_pos[1]
                print("코코코 레드코~~", nose_x, " ", nose_y)
            cv2.circle(frame, pt_pos, 2, (0, 255, 0), -1)
            num = num + 1
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()),
                      (0, 0, 255), 3)

    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == ord('1'):
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
    ##수아꺼 끝

    # frame 출력
    cv2.imshow("frame", frame)
