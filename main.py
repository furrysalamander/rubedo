import cv2
import numpy as np
from glob import glob
from collections.abc import Iterable
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_GRAPH = False
OUTPUT_FRAMES = False

def brightest_average(pixel_values: np.ndarray):
    brightest_pixels = np.argsort(pixel_values)[-3:]
    line_brightest_x = np.average(brightest_pixels)
    return line_brightest_x


def weighted_average(pixel_values: np.ndarray):
    normalized_values = pixel_values / 255
    adjusted_values = normalized_values ** 200
    x_values = np.arange(adjusted_values.size)
    return np.average(x_values, weights=adjusted_values)


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
    # return algorithms["brightest_avg"](pixel_values)
    # return algorithms["count_non_zero"](pixel_values)
    # return algorithms["first_non_zero"](pixel_values)
    return algorithms["count_non_zero"](pixel_values)


fig = plt.figure()
from matplotlib.animation import FFMpegWriter
writer = FFMpegWriter(fps=30)
plt.ylim([0, 200])
l = None

def graph_frame(pixel_values: np.ndarray, output_file: str):
    # fig.
    return
    # plt.figure()
    global l
    if l is None:
       l, = plt.plot(pixel_values)
    else:
        x = np.arange(len(pixel_values))
        l.set_data(x, pixel_values)
    # writer.grab_frame()
    # plt.savefig(output_file)
    # plt.close()
    return


def crop_frame(frame):
    mid_y = 720//2 + 15
    mid_x = 1280//2 + 30
    frame = frame[mid_y-50:mid_y+50, mid_x+100:mid_x+300]
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


def compute_score_for_frame(x_values: Iterable):
    return np.std(x_values)


def compute_height_map(video_file):
    video_data = cv2.VideoCapture(video_file)
    frames = []
    while video_data.isOpened():
        ret, frame = video_data.read()
        if not ret:
            break

        frame = crop_frame(frame)
        frame = preprocess_frame(frame)
        # frame = apply_gaussian_blur(frame)

        laser_x_values = []

        for line in frame:
            if line.max() > 0:
                laser_x_val = compute_x_value(line)
                laser_x_values.append(laser_x_val)
        frames.append(laser_x_values)
    return frames


def graph_height_map(frames):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    points = []
    for y, line_data in enumerate(frames):
        for x, z in enumerate(line_data):
            points.append(
                (x, y, z)
            )
    x, y, z = zip(*points)
    x, y, z = np.array(x), np.array(y), np.array(z)
    ax.scatter(x, y, z)
    fig.savefig("surface_map.png")


def main():
    ranking = []

    # i = 0
    for video_file in sorted(glob("sample_data2/*")):
        # if i < 6:
        #     i += 1
        #     continue

        # height_data = compute_height_map(video_file)
        # graph_height_map(height_data)

        # return

        fig.suptitle(video_file)
        video_data = cv2.VideoCapture(video_file)

        # out = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, (400,400))

        frame_index = 0

        video_std = []
        while video_data.isOpened():
            ret, frame = video_data.read()
            if not ret:
                break

            frame = crop_frame(frame)
            frame = preprocess_frame(frame)
            # frame = apply_gaussian_blur(frame)

            laser_x_values = []

            for line in frame:
                if line.max() > 0:
                    laser_x_val = compute_x_value(line)
                    laser_x_values.append(laser_x_val)
            
            if OUTPUT_GRAPH:
                graph_frame(laser_x_values, f"graphs/{Path(video_file).stem}-{frame_index}.png")

            # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            # out.write(gray)
            if OUTPUT_FRAMES:
                cv2.imwrite(f"frame_data/{Path(video_file).stem}-{frame_index}.png", frame)

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
        # return

    print('\nSCORES\n')

    [ print(x) for x in sorted(ranking, key=lambda x: x[1])]


if __name__=="__main__":
    main()
