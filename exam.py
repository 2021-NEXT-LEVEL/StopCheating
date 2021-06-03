import dlib
import cv2 as cv
import numpy as np
import math
from detect import *
from alert import print_alert


def startExam():  # [시험 시작] 버튼 클릭 시 부정행위 감지 프로그램 시작
    alert_flag = 0
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    cap = cv.VideoCapture(0)

    ALL = list(range(0, 68))
    index = ALL

    up_lip_x, up_lip_y, down_lip_x, down_lip_y = 0, 0, 0, 0
    right_lip_x, right_lip_y, left_lip_x, left_lip_y = 0, 0, 0, 0

    while True:
        ret, img_frame = cap.read()
        img_gray = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)
        dets = detector(img_gray, 1)
        
        # Algorithm 2 - face detection using Haar Cascade
        # if detectWithHaar(img_gray, img_frame) > 1:
        #    alert_flag = 1

        for face in dets:
            # Algorithm 1 - face detection using Dlib Face Landmark
            if len(dets) > 1:  # case == 1 -> 두 명 이상 감지
                alert_flag = 1
            
            shape = predictor(img_frame, face)  # 얼굴에서 68개 점 찾기
            list_points = []
            for p in shape.parts():
                list_points.append([p.x, p.y])

            list_points = np.array(list_points)
            num = 0
            left_eye_x = 0
            left_eye_y = 0
            right_eye_x = 0
            right_eye_y = 0

            for i, pt in enumerate(list_points[index]):
                pt_pos = (pt[0], pt[1])
                # chin detect points
                if num == 29:
                    nose_x = pt_pos[0]
                    nose_y = pt_pos[1]
                if num == 37 or num == 40:
                    left_eye_x = left_eye_x + pt_pos[0]
                    left_eye_y = left_eye_y + pt_pos[1]
                if num == 41:
                    left_eye_x = left_eye_x // 2
                    left_eye_y = left_eye_y // 2
                if num == 44 or num == 47:
                    right_eye_x = right_eye_x + pt_pos[0]
                    right_eye_y = right_eye_y + pt_pos[1]
                if num == 48:
                    right_eye_x = right_eye_x // 2
                    right_eye_y = right_eye_y // 2
                # mouth detect points
                if i == 51:
                    up_lip_x = pt_pos[0]
                    up_lip_y = pt_pos[1]
                if i == 57:
                    down_lip_x = pt_pos[0]
                    down_lip_y = pt_pos[1]
                if i == 48:
                    right_lip_x = pt_pos[0]
                    right_lip_y = pt_pos[1]
                if i == 54:
                    left_lip_x = pt_pos[0]
                    left_lip_y = pt_pos[1]
                cv.circle(img_frame, pt_pos, 2, (0, 255, 0), -1)
                num = num + 1

            cv.rectangle(img_frame, (face.left(), face.top()), (face.right(), face.bottom()),
                         (0, 0, 255), 3)

            gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], shape, img_frame, img_gray)
            gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], shape, img_frame, img_gray)
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2

            if gaze_ratio < 0.3 or gaze_ratio > 3.3:
                alert_flag = 4

        # chin detect
        nose_to_eye_left_x = nose_x - left_eye_x
        nose_to_eye_left_y = nose_y - left_eye_y
        nose_to_eye_right_x = nose_x - right_eye_x
        nose_to_eye_right_y = nose_y - right_eye_y
        norm_left = math.sqrt(nose_to_eye_left_x ** 2 + nose_to_eye_left_y ** 2)
        norm_right = math.sqrt(nose_to_eye_right_x ** 2 + nose_to_eye_right_y ** 2)
        if abs(norm_left - norm_right) >= 15:
            alert_flag = 2

        # mouth detect
        height = up_lip_y - down_lip_y
        width = right_lip_x - left_lip_x
        ratio = height / width
        if ratio > 0.8:
            alert_flag = 3

        if alert_flag != 0:
            alert_flag = print_alert(alert_flag)

        key = cv.waitKey(1)

        cv.imshow('result', img_frame)

        if key == 27:
            break

    cap.release()
