import cv2
import pyvirtualcam
import numpy as np
import time

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)


def toRGBA(frame):
    b_channel, g_channel, r_channel = cv2.split(frame)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50  # creating a dummy alpha channel image.

    rgba = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))

    return rgba




with pyvirtualcam.Camera(width=480, height=270, fps=30) as cam:
    while True:
        _, frame = cap.read()

        frame = frame[45:315, 80:560]

        cv2.imshow('test', frame)

        cam.send(toRGBA(frame))
        cam.sleep_until_next_frame()


        if cv2.waitKey(1) == ord('q'):
            break



cap.release()
cv2.destroyAllWindows()
