#!/usr/bin/python3
import cv2
import numpy as np
from glob import glob
from pathlib import Path

from processing import *
from visualization import graph_height_map
from analysis import compute_x_value


def generate_height_data_for_frame(frame: np.ndarray):
    frame = crop_frame(frame)
    frame = preprocess_frame(frame)
    frame = apply_gaussian_blur(frame)

    frame_height_data = np.ndarray(frame.shape[0])

    for index, line in enumerate(frame):
        # if line.max() > 0:
        laser_x_val = compute_x_value(line)
        frame_height_data[index] = laser_x_val

    return frame_height_data


def generate_height_data_from_video(video_file: str):
    video = cv2.VideoCapture(video_file)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    height_data: np.ndarray = np.ndarray((frame_count, FRAME_SIZE_Y))

    frame_index = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        
        height_data[frame_index] = generate_height_data_for_frame(frame)
        
        frame_index += 1

    return height_data


def compute_score_from_heightmap(height_map: np.ndarray):
    sum_of_scores = 0

    for line in height_map.transpose():
        sum_of_scores += np.std(line)
    return sum_of_scores


def main():
    ranking = []

    # frame_score = compute_score_for_frame(laser_x_values)
    # print(frame_index, frame_std)

    # i = 0
    for video_file in sorted(glob("sample_data2/*")):
        # if i < 6:
        #     i += 1
        #     continue
        video_height_data = generate_height_data_from_video(video_file)

        if OUTPUT_HEIGHT_MAPS:
            graph_height_map(video_height_data, f"height_maps/{Path(video_file).stem}.png")

        score = compute_score_from_heightmap(video_height_data)
        # height_data = compute_height_map(video_file)
        # graph_height_map(height_data)

        # return

        # fig.suptitle(video_file)

        # out = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, (400,400))

        frame_index = 0

        # video_std = []
            # red_line = cv2.cvtColor(red_line, cv2.COLOR_GRAY2BGR)
            # out.write(red_line)
        # exit()
        # out.release()
        # print(np.std(video_std))
        print(video_file, score)

        ranking.append((video_file, score))
        # return

    print('\nSCORES\n')

    [ print(x) for x in sorted(ranking, key=lambda x: x[1])]


if __name__=="__main__":
    main()
