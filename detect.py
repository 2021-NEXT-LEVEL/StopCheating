import cv2 as cv
import numpy as np


def get_gaze_ratio(eye_points, facial_landmarks, frame, gray):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)],
                               np.int32)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv.polylines(mask, [left_eye_region], True, 255, 2)
    cv.fillPoly(mask, [left_eye_region], 255)
    eye = cv.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv.threshold(gray_eye, 70, 255, cv.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio


def detectWithHaar(img_gray, img_frame):
    face_cascade = cv.CascadeClassifier(
        '/opt/homebrew/Cellar/opencv/4.5.2_1/data/haarcascades/haarcascade_frontalcatface.xml')
    # For Windows users
    # "C:\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_alt.xml";

    count = 0
    faces = face_cascade.detectMultiScale(img_gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv.rectangle(img_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1
        print(count)

    return count