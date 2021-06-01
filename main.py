import dlib
import cv2 as cv
import numpy as np
from tkinter import *
import tkinter.messagebox
import math
from datetime import datetime

# [시험 시작] 버튼 클릭 시 프로그램 실행 시 시작 여부를 사용자에게 물어봄
def askStartExam():
    MsgBox = tkinter.messagebox.askquestion("Message", "시험을 시작하시겠습니까?")
    if MsgBox == 'yes':
        startExam()
    else:
        return


# [시험 종료] 버튼 클릭 시 시험을 종료시킴
def askFinishExam():
    MsgBox = tkinter.messagebox.askquestion("Message", "시험을 종료하시겠습니까?")
    if MsgBox == 'yes':
        window.destroy()


# 부정행위 감지 시 alert
def alert(case):
    now = datetime.now()
    if case == 1:
        #tkinter.messagebox.showinfo("Alert", "두 명 이상 감지되었습니다.")
        print("alert log[2명이상] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    elif case == 2:
        #tkinter.messagebox.showinfo("Alert", "고개 돌림이 감지되었습니다.")
        print("alert log[고개돌림] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    elif case == 3:
        #tkinter.messagebox.showinfo("Alert", "대화가 감지되었습니다.")
        print("alert log[대화] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    elif case == 4:
        tkinter.messagebox.showinfo("Alert", "화면 밖 응시가 감지되었습니다.")
        print("alert log[화면 밖 응시] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))



# 얼굴에서 눈을 파악하여 공막과 각막의 위치를 확인하여 시선 계산
def get_gaze_ratio(eye_points, facial_landmarks, frame, gray):
    # 왼쪽 눈의 움직임 탐지 -> 양쪽 눈은 같이 움직이기 때문에, 한 쪽만 탐색
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)],
                               np.int32)

    # 기존 웹캠 이미지에서 eye point를 사용하여 눈 영역 남기고 모두 제거
    height, width, _ = frame.shape  # frame 크기 저장 2차원 저장
    mask = np.zeros((height, width), np.uint8)  # height x width 사이즈의 0행렬
    cv.polylines(mask, [left_eye_region], True, 255, 2)  # mask 이미지에 왼쪽 눈 좌표에 Black 도형
    cv.fillPoly(mask, [left_eye_region], 255)  # 왼쪽 눈 좌표에 맞는 색칠된 Black 도형
    eye = cv.bitwise_and(gray, gray, mask=mask)  # gray 이미지에 눈만 칠해진 mask와 and연산을 해서 눈 이미지만 남김

    # 왼쪽 눈의 각 꼭짓점 좌표 저장
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])
    gray_eye = eye[min_y: max_y, min_x: max_x]

    # 눈 이미지에서 동공과 나머지 눈 영역으로 이진화
    _, threshold_eye = cv.threshold(gray_eye, 70, 255, cv.THRESH_BINARY)  # t값보다 크면 value, 작으면 0
    height, width = threshold_eye.shape

    # 눈의 중앙을 기점으로, 왼쪽/오른족으로 나눠서 흰 부분의 비율 계산
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv.countNonZero(right_side_threshold)

    if left_side_white == 0:  # 왼쪽에 검은자만 있으면 ratio = 1(왼쪽 시선)
        gaze_ratio = 1
    elif right_side_white == 0:  # 오른쪽에 검은자만 있으면 ratio = 6(오른쪽 시선)
        gaze_ratio = 6
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio


# [시험 시작] 버튼 클릭 시 부정행위 감지 프로그램 시작
def startExam():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    cap = cv.VideoCapture(0)

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

    up_lip_x, up_lip_y, down_lip_x, down_lip_y = 0, 0, 0, 0
    right_lip_x, right_lip_y, left_lip_x, left_lip_y = 0, 0, 0, 0

    while True:
        ret, img_frame = cap.read()
        img_gray = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)
        dets = detector(img_gray, 1)

        for face in dets:
            if len(dets) > 1:  # case == 1 -> 두 명 이상 감지
                alert(1)
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
                if (i == 52):
                    up_lip_x = pt_pos[0]
                    up_lip_y = pt_pos[1]
                if (i == 58):
                    down_lip_x = pt_pos[0]
                    down_lip_y = pt_pos[1]
                if (i == 49):
                    right_lip_x = pt_pos[0]
                    right_lip_y = pt_pos[1]
                if (i == 55):
                    left_lip_x = pt_pos[0]
                    left_lip_y = pt_pos[1]
                cv.circle(img_frame, pt_pos, 2, (0, 255, 0), -1)
                num = num + 1

            cv.rectangle(img_frame, (face.left(), face.top()), (face.right(), face.bottom()),
                         (0, 0, 255), 3)

            # 눈 point를 사용하여 해당 위치에서 공막/각막의 위치로 시선 탐지
            gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], shape, img_frame, img_gray)
            gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], shape, img_frame, img_gray)
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2

            gaze_str = str(gaze_ratio)
            cv.putText(img_frame, gaze_str, (0, 100), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 3, (0,255,0))

            if gaze_ratio < 0.27 or gaze_ratio > 5.5: # ratio가 너무 낮으면 화면 밖 오른쪽, ratio가 너무 낮으면 화면 밖 왼쪽을 응시했다고 간주하고 알람
                alert(4)


        # chin detect
        nose_to_eye_left_x = nose_x - left_eye_x
        nose_to_eye_left_y = nose_y - left_eye_y
        nose_to_eye_right_x = nose_x - right_eye_x
        nose_to_eye_right_y = nose_y - right_eye_y
        norm_left = math.sqrt(nose_to_eye_left_x ** 2 + nose_to_eye_left_y ** 2)
        norm_right = math.sqrt(nose_to_eye_right_x ** 2 + nose_to_eye_right_y ** 2)
        if abs(norm_left - norm_right) >= 15:
            alert(2)

        # mouth detect
        height = up_lip_y - down_lip_y
        width = right_lip_x - left_lip_x
        ratio = height / width
        if ratio > 0.8:
            alert(3)

        key = cv.waitKey(1)

        cv.imshow('result', img_frame)

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


if __name__ == "__main__":
    window = Tk()
    window.title("온라인 시험 부정행위 방지 프로그램")

    base_frame = Frame(window)
    base_frame.pack()

    btn_start_exam = Button(base_frame, text="시험 시작", width="20", command=askStartExam)
    btn_start_exam.pack(pady="10")

    btn_finish_exam = Button(base_frame, text="시험 종료", width="20", command=askFinishExam)
    btn_finish_exam.pack(pady="10")

    window.mainloop()
    window.after(100000, askFinishExam)  # 시험시간 : 1분 후 종료