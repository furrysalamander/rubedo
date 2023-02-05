import cv2
import numpy as np
from glob import glob

# result = cv2.imread("2023-01-16-213226.jpg")
ranking = []

for video_file in sorted(glob("sample_data2/*")):
    video_data = cv2.VideoCapture(video_file)

    out = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, (400,400))

    mid_y = 720//2
    mid_x = 1280//2


    frame_index = 0

    video_std = []
    while video_data.isOpened():
        ret, frame = video_data.read()
        if not ret:
            break
        frame = frame[mid_y-100:mid_y+100, mid_x+100:mid_x+300]

        lowerb = np.array([0, 0, 120])
        upperb = np.array([255, 255, 255])
        red_line = cv2.inRange(frame, lowerb, upperb)

        masked_video = cv2.bitwise_and(frame,frame,mask = red_line)
        # cv2.imwrite("test.png", masked_video)
        # exit()
        # out.write(masked_video)

        gray = cv2.cvtColor(masked_video, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)
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
            # out.write(gray)
            # cv2.imwrite(f"frame_data/{frame_index}.png", gray)

            frame_std = np.std(frame_brightest_x)
            # print(frame_index, frame_std)
            video_std.append(frame_std)
            frame_index += 1
            # red_line = cv2.cvtColor(red_line, cv2.COLOR_GRAY2BGR)
            # out.write(red_line)
    # out.release()
    print(video_file, np.std(video_std))

    # if True:
    # # if "line7.mp4" in video_file:
    #     break

    ranking.append((video_file, np.std(video_std)))

print('\nSCORES\n')

[ print(x) for x in sorted(ranking, key=lambda x: x[1])]




# cv2.imwrite("test.png", frame)

# line starts on frame 12
# line ends on frame 32
# line starts on frame 41
# line ends on 61
# line starts on 70
# line ends on 90
# line starts on 99
# line ends on 119
