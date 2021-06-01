import tkinter.messagebox
from tkinter import *
from datetime import *
from exam import *
from alert import alert_list
from alert import alert_count


def askStartExam():  # [시험 시작] 프로그램 실행 시 시작 여부를 사용자에게 물어봄
    MsgBox = tkinter.messagebox.askquestion("Message", "시험을 시작하시겠습니까?")
    if MsgBox == 'yes':
        now = datetime.now()
        alert_list.append("%s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
        startExam()
    else:
        return


def askFinishExam():  # [시험 종료] 시험을 종료시킴
    MsgBox = tkinter.messagebox.askquestion("Message", "시험을 종료하시겠습니까?")
    if MsgBox == 'yes':
        now = datetime.now()
        alert_list.append("%s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
        window.destroy()

        print("> Logs")
        for i in range(1, len(alert_list)-1):
            print(alert_list[i])
        start = alert_list[0]
        end = alert_list[len(alert_list)-1]
        print("------------------------")
        print(" 2명 이상 감지:", alert_count[0], "회")
        print(" 고개 돌림 감지:", alert_count[1], "회")
        print(" 대화 감지:", alert_count[2], "회")
        print(" 화면 밖 응시 감지:", alert_count[3], "회")
        print("------------------------")


if __name__ == "__main__":
    window = Tk()
    window.title("온라인 시험 부정행위 방지 프로그램")

    base_frame = Frame(window)
    base_frame.pack()

    btn_start_exam = Button(base_frame, text="시험 시작", width="20", command=askStartExam)
    btn_start_exam.pack(pady="10")

    btn_finish_exam = Button(base_frame, text="시험 종료", width="20", command=askFinishExam)
    btn_finish_exam.pack(pady="10")

    info = "시험 시 주의 사항\n\n " \
           "1. 해당 시험은 시험 참여인원, 시선처리, 얼굴 방향, 대화를 감지합니다.\n" \
           "2. [시험 시작] 버튼을 눌러 시험을 시작합니다.\n" \
           "3. 시험 도중 경고창이 뜨면 [확인] 버튼을 눌러 시험을 재진행 하십시오.\n" \
           "4. 시험 종료 시 키보드에서 ESC을 누른 후, [시험 종료] 버튼을 눌러 정상 종료하십시오."
    info_message = tkinter.messagebox.showinfo("Info", info)

    window.mainloop()

