import cv2
import numpy as np

# result = cv2.imread("2023-01-16-213226.jpg")

video_data = cv2.VideoCapture("sample_video.mp4")

out = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 14.97, (400,400))

mid_y = 2592//2
mid_x = 1944//2

frame_index = 0

while video_data.isOpened():
    ret, frame = video_data.read()
    if not ret:
        break
    frame = frame[mid_y-200:mid_y+200, mid_x+400:mid_x+800]

    lowerb = np.array([0, 0, 150])
    upperb = np.array([255, 255, 255])
    red_line = cv2.inRange(frame, lowerb, upperb)

    masked_video = cv2.bitwise_and(frame,frame,mask = red_line)
    # out.write(masked_video)

    gray = cv2.cvtColor(masked_video, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    
    frame_brightest_x = []

    for line in gray:
        # find the 4 brightest pixels
        if line.max() > 0:
            brightest_pixels = np.argsort(line)[-4:]
            line_brightest_x = np.average(brightest_pixels)
            frame_brightest_x.append(line_brightest_x)
    
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    if len(frame_brightest_x) > 0:
        out.write(gray)
        cv2.imwrite(f"frame_data/{frame_index}.png", gray)

        print(frame_index, np.std(frame_brightest_x))
        frame_index += 1
        # red_line = cv2.cvtColor(red_line, cv2.COLOR_GRAY2BGR)
        # out.write(red_line)


out.release()
# cv2.imwrite("test.png", frame)

# line starts on frame 12
# line ends on frame 32
# line starts on frame 41
# line ends on 61
# line starts on 70
# line ends on 90
# line starts on 99
# line ends on 119
