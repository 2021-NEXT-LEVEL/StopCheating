import tkinter.messagebox
from datetime import *


alert_list = []
alert_count = [0, 0, 0, 0]


def print_alert(case):  # 부정행위 감지 시 alert
    now = datetime.now()
    if case == 1:
        tkinter.messagebox.showinfo("Alert", "두 명 이상 감지되었습니다.")
        alert_count[0] += 1
        alert_list.append("alert log[2명이상] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    elif case == 2:
        tkinter.messagebox.showinfo("Alert", "고개 돌림이 감지되었습니다.")
        alert_count[1] += 1
        alert_list.append("alert log[고개돌림] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    elif case == 3:
        alert_count[2] += 1
        tkinter.messagebox.showinfo("Alert", "대화가 감지되었습니다.")
        alert_list.append("alert log[대화] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    elif case == 4:
        alert_count[3] += 1
        tkinter.messagebox.showinfo("Alert", "화면 밖 응시가 감지되었습니다.")
        alert_list.append("alert log[화면 밖 응시] : %s년 %s월 %s일 %s시 %s분 %s초.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
    return 0
