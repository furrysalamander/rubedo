import cv2
import numpy as np
from glob import glob
from collections.abc import Iterable
import matplotlib.pyplot as plt
from pathlib import Path


def brightest_average(pixel_values: np.ndarray):
    brightest_pixels = np.argsort(pixel_values)[-3:]
    line_brightest_x = np.average(brightest_pixels)
    return line_brightest_x


def weighted_average(pixel_values: np.ndarray):
    normalized_values = pixel_values / 255
    adjusted_values = normalized_values
    x_values = np.arange(pixel_values.size)
    return np.average(x_values, weights=pixel_values)


def first_non_zero(pixel_values: np.ndarray):
    return np.nonzero(pixel_values)[0][0]

def count_non_zero(pixel_values: np.ndarray):
    return np.count_nonzero(pixel_values)


def compute_x_value(pixel_values: np.ndarray):
    algorithms = {
        "brightest_avg": brightest_average,
        "weighted_avg": weighted_average,
        "first_non_zero": first_non_zero,
        "count_non_zero": count_non_zero,
    }
    return algorithms["brightest_avg"](pixel_values)
    # return algorithms["count_non_zero"](pixel_values)
    # return algorithms["first_non_zero"](pixel_values)
    # return algorithms["weighted_avg"](pixel_values)


def graph_frame(pixel_values: np.ndarray, output_file: str):
    return
    plt.figure()
    plt.plot(pixel_values)
    plt.ylim([0, 200])
    plt.savefig(output_file)
    plt.close()


def compute_score_for_frame(x_values: Iterable):
    return np.std(x_values)


def main():
    ranking = []

    for video_file in sorted(glob("sample_data2/*")):
        video_data = cv2.VideoCapture(video_file)

        out = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, (400,400))

        mid_y = 720//2 + 15
        mid_x = 1280//2 + 30

        frame_index = 0

        video_std = []
        while video_data.isOpened():
            ret, frame = video_data.read()
            if not ret:
                break
            frame = frame[mid_y-50:mid_y+50, mid_x+100:mid_x+300]

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
            
            laser_x_values = []

            for line in gray:
                # find the 4 brightest pixels
                if line.max() > 0:
                    laser_x_val = compute_x_value(line)
                    laser_x_values.append(laser_x_val)
            
            graph_frame(laser_x_values, f"graphs/{Path(video_file).stem}-{frame_index}.png")

            # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            # out.write(gray)
            cv2.imwrite(f"frame_data/{Path(video_file).stem}-{frame_index}.png", gray)

            frame_score = compute_score_for_frame(laser_x_values)
            # print(frame_index, frame_std)
            video_std.append(frame_score)
            frame_index += 1
            # red_line = cv2.cvtColor(red_line, cv2.COLOR_GRAY2BGR)
            # out.write(red_line)
        # exit()
        # out.release()
        print(np.std(video_std))

        ranking.append((video_file, np.std(video_std)))

    print('\nSCORES\n')

    [ print(x) for x in sorted(ranking, key=lambda x: x[1])]


if __name__=="__main__":
    main()
