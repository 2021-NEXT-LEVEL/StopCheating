import dlib
import cv2 as cv
import numpy as np
from tkinter import *
import tkinter.messagebox
from datetime import datetime


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
    if case == 1:
        tkinter.messagebox.showinfo("Alert", "두 명 이상 감지되었습니다.")
    now = datetime.now()
    print("alert log : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))


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

    while True:
        ret, img_frame = cap.read()
        img_gray = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)
        dets = detector(img_gray, 1)

        for face in dets:
            if len(dets) > 1: # case == 1 -> 두 명 이상 감지
                alert(1)
            shape = predictor(img_frame, face)  # 얼굴에서 68개 점 찾기
            list_points = []
            for p in shape.parts():
                list_points.append([p.x, p.y])

            list_points = np.array(list_points)

            for i, pt in enumerate(list_points[index]):
                pt_pos = (pt[0], pt[1])
                cv.circle(img_frame, pt_pos, 2, (0, 255, 0), -1)

            cv.rectangle(img_frame, (face.left(), face.top()), (face.right(), face.bottom()),
                         (0, 0, 255), 3)
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
    window.after(100000, askFinishExam) # 시험시간 : 1분 후 종료
