import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from constants import *

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

def graph_height_map(z_data: np.ndarray, output_file: str):
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    fig, ax = plt.subplots()

    # points = []
    # for y, line_data in enumerate(frames):
    #     for x, z in enumerate(line_data):
    #         points.append(
    #             (x, y, z)
    #         )
    # x, y, z = zip(*points)
    # x, y, z = np.array(x), np.array(y), np.array(z)
    y = np.arange(len(z_data))
    x = np.arange(len(z_data[0]))
    (x ,y) = np.meshgrid(x,y)

    # ax.plot_surface(x, y, z_data,cmap=cm.coolwarm,linewidth=0, antialiased=False)
    ax.pcolormesh(x, y, z_data, cmap='RdBu')
    # ax.scatter(x, y, z)
    fig.savefig(output_file)


def generate_graph_from_heightmap():
    if OUTPUT_GRAPH:
        graph_frame(laser_x_values, f"graphs/{Path(video_file).stem}-{frame_index}.png")
    pass

def generate_frames_from_heightmap():
    if OUTPUT_FRAMES:
        cv2.imwrite(f"frame_data/{Path(video_file).stem}-{frame_index}.png", frame)
    pass




fig = plt.figure()
from matplotlib.animation import FFMpegWriter
writer = FFMpegWriter(fps=30)
plt.ylim([0, 200])
l = None
