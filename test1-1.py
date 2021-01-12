import cv2
import pyvirtualcam
import numpy as np
import time

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

cam = pyvirtualcam.Camera(width=480, height=270, fps=30)


def toRGBA(frame):
    b_channel, g_channel, r_channel = cv2.split(frame)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50  # creating a dummy alpha channel image.

    rgba = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))

    return rgba



def virtual_cam():
    global rec, cam

    i = 0
    N = len(rec)
    lag_cnt = 0
    while True:
        cam.send(rec[i])
        cv2.imshow('test', rec[i])
        time.sleep(1/30)

        i += 1
        if i == N:
            if lag_cnt < 20:
                lag_cnt += 1
                i = N-1

            else:
                lag_cnt
                i = 0


        if cv2.waitKey(1) == ord('q'):
            print('End Virtual Cam')
            lagging_effect(rec[i])
            break




def lagging_effect(frame):
    global cam
    for i in range(20):
        cam.send(frame)
        cv2.imshow('test', frame)
        time.sleep(1/30)


rec = []
rec_status = False


while True:
    _, frame = cap.read()

    frame = frame[45:315, 80:560]

    cv2.imshow('test', frame)

    real_frame = toRGBA(frame)
    cam.send(real_frame)
    cam.sleep_until_next_frame()



    # if cv2.waitKey(1) == ord('q'):
    #    break



    if cv2.waitKey(1) == ord('w'):
        print('Virtual Cam Start')
        rec_status = False
        virtual_cam()


    if rec_status:
        rec.append(real_frame)

        if cv2.waitKey(1) == ord('e'):
            print('Stop Recording')
            rec_status = False

    else:
        if cv2.waitKey(1) == ord('r'):
            print('Start Recording')
            rec = []
            rec_status = True

    if cv2.waitKey(1) == ord('z'):
        break


cam.close()
cap.release()
cv2.destroyAllWindows()
