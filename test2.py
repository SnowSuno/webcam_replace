import cv2
import pyvirtualcam
import numpy as np
import time
import _thread


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)


def toRGBA(frame):
    b_channel, g_channel, r_channel = cv2.split(frame)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50  # creating a dummy alpha channel image.

    rgba = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))

    return rgba


rec = []


def real_cam():
    global cam, rec
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    rec_status = 0
    while True:
        _, frame = cap.read()

        frame = frame[45:315, 80:560]

        cv2.imshow('test', frame)


        real_frame = toRGBA(frame)
        cam.send(real_frame)
        cam.sleep_until_next_frame()


        if cv2.waitKey(1) == ord('r'):
            rec = []
            rec_status = 1

        if cv2.waitKey(1) == ord('e'):
            rec_status = 0
            virtual_cam()

        if rec_status == 1:
            rec.append(real_frame)


def virtual_cam():
    global rec, cam

    while True:
        current_frame = rec[0]
        for virtual_frame in rec:
            current_frame = virtual_frame
            cam.send(virtual_frame)
            cam.sleep_until_next_frame()

            if cv2.waitKey(1) == ord('q'):
                lagging_effect(cam, current_frame)
                break

        lagging_effect(cam, current_frame)




def lagging_effect(frame):
    global cam
    for i in range(10):
        cam.send(frame)
        cam.sleep_until_next_frame()


with pyvirtualcam.Camera(width=480, height=270, fps=30) as cam:
    real_cam()



cap.release()
cv2.destroyAllWindows()
