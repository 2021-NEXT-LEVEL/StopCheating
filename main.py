import dlib
import numpy as np
import cv2 as cv
from gaze_tracking import GazeTracking  # 눈동자 추적 library
import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import math

eye_r_count = 0
eye_l_count = 0

def askStartExam():  # [시험 시작] 프로그램 실행 시 시작 여부를 사용자에게 물어봄
    MsgBox = tkinter.messagebox.askquestion("Message", "시험을 시작하시겠습니까?")
    if MsgBox == 'yes':
        startExam()
    else:
        return


def askFinishExam():  # [시험 종료] 시험을 종료시킴
    MsgBox = tkinter.messagebox.askquestion("Message", "시험을 종료하시겠습니까?")
    if MsgBox == 'yes':
        window.destroy()


def alert(case):  # 부정행위 감지 시 alert
    now = datetime.now()
    if case == 1:
        tkinter.messagebox.showinfo("Alert", "두 명 이상 감지되었습니다.")
        print("alert log[2명이상] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    elif case == 2:
        tkinter.messagebox.showinfo("Alert", "고개 돌림이 감지되었습니다.")
        print("alert log[고개돌림] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    elif case == 3:
        tkinter.messagebox.showinfo("Alert", "대화가 감지되었습니다.")
        print("alert log[대화] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))


def startExam():  # [시험 시작] 버튼 클릭 시 부정행위 감지 프로그램 시작
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

    up_lip_x, up_lip_y, down_lip_x, down_lip_y = 0, 0, 0, 0;
    right_lip_x, right_lip_y, left_lip_x, left_lip_y = 0, 0, 0, 0;

    while True:
        ret, frame = cap.read()
        img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        dets = detector(img_gray, 1)
        
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
        cv.putText(frame, text, (90, 60), cv.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        # 눈동자 위치 출력
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        for face in dets:
            if len(dets) > 1:  # case == 1 -> 두 명 이상 감지
                alert(1)
            shape = predictor(frame, face)  # 얼굴에서 68개 점 찾기
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

                cv.circle(frame, pt_pos, 2, (0, 255, 0), -1)
                num = num + 1

            cv.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()),
                         (0, 0, 255), 3)

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
        height = up_lip_y - down_lip_y;
        width = right_lip_x - left_lip_x;
        ratio = height / width;
        print("ratio: ",ratio);
        if ratio > 0.8:
            alert(3)
            
        key = cv.waitKey(1)
        cv.imshow('result', frame)
        if key == 27:
            break
            
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
