from constants import *
import cv2
import numpy as np

def crop_frame(frame):
    mid_y = 720//2 + Y_OFFSET
    mid_x = 1280//2 + X_OFFSET
    half_y = FRAME_SIZE_Y / 2
    half_x = FRAME_SIZE_X / 2
    frame = frame[int(mid_y-half_y):int(mid_y+half_y), int(mid_x-half_x):int(mid_x+half_x)]
    return frame


def preprocess_frame(frame):
    lowerb = np.array([0, 0, 120])
    upperb = np.array([255, 255, 255])
    red_line = cv2.inRange(frame, lowerb, upperb)

    masked_video = cv2.bitwise_and(frame,frame,mask = red_line)

    gray = cv2.cvtColor(masked_video, cv2.COLOR_BGR2GRAY)
    return gray


def apply_gaussian_blur(frame):
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    return frame

