# import cv2
import numpy as np
import matplotlib.pyplot as plt
from pa_result import PaResult
from pathlib import Path

from constants import *


## FIXME:
#
# This WHOLE file is currently a broken mess.  Needs to be cleaned up and fixed.
# 
#
#

def generate_color_map(pa_result: PaResult):
    fig, ax = plt.subplots()

    y = np.arange(len(pa_result.height_data))
    x = np.arange(len(pa_result.height_data[0]))
    (x ,y) = np.meshgrid(x,y)

    # ax.plot_surface(x, y, z_data,cmap=cm.coolwarm,linewidth=0, antialiased=False)
    ax.pcolormesh(x, y, pa_result.height_data, cmap='RdBu')
    # ax.scatter(x, y, z)
    return fig

def generate_cross_section_video():
    pass

def generate_cross_sections():
    pass

def generate_3d_height_map(pa_result: PaResult):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    y = np.arange(len(pa_result.height_data))
    x = np.arange(len(pa_result.height_data[0]))
    (x ,y) = np.meshgrid(x,y)
    ax.plot_surface(x, y, pa_result.height_data, cmap="RdBu")
    ax.set_zlim3d(60, 100)

    return fig


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


def generate_graphs_for_pa_results(pa_data: PaResult):
    graph_frame(laser_x_values, f"graphs/{Path(video_file).stem}-{frame_index}.png")


def generate_frames_from_heightmap(pa_data: PaResult):
    cv2.imwrite(f"frame_data/{Path(video_file).stem}-{frame_index}.png", frame)


# fig = plt.figure()
# from matplotlib.animation import FFMpegWriter
# writer = FFMpegWriter(fps=30)
# plt.ylim([0, 200])
# l = None
