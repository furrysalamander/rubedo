# import cv2
import numpy as np
import matplotlib.pyplot as plt
from pa_result import PaResult
from pathlib import Path

from constants import *

def generate_color_map(pa_result: PaResult):
    fig, ax = plt.subplots()

    x = np.arange(len(pa_result.height_data))
    y = np.arange(len(pa_result.height_data[0]))
    (x ,y) = np.meshgrid(x,y)

    ax.pcolormesh(x, y, np.transpose(pa_result.height_data), cmap='plasma')
    ax.set_xlabel("X Value (Frame)")
    ax.set_ylabel("Y Value (Pixel)")

    ax.set_title("Height Map", fontsize=10)
    return fig


def generate_3d_height_map(pa_result: PaResult):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    y = np.arange(len(pa_result.height_data))
    x = np.arange(len(pa_result.height_data[0]))
    (x ,y) = np.meshgrid(x,y)
    ax.plot_surface(x, y, pa_result.height_data, cmap="plasma")
    ax.set_zlim3d(10, 50)

    ax.set_ylabel("X Value (Frame)")
    ax.set_xlabel("Y Value (Pixel)")
    ax.set_zlabel("Height (mm)")

    ax.set_title("3D Height Map", fontsize=10, y=1)
    
    fig.tight_layout()

    return fig

def generate_cross_section_video():
    pass

def generate_cross_sections():
    pass

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


def generate_graphs_for_pa_results(pa_data: PaResult):
    graph_frame(laser_x_values, f"graphs/{Path(video_file).stem}-{frame_index}.png")


def generate_frames_from_heightmap(pa_data: PaResult):
    cv2.imwrite(f"frame_data/{Path(video_file).stem}-{frame_index}.png", frame)


# fig = plt.figure()
# from matplotlib.animation import FFMpegWriter
# writer = FFMpegWriter(fps=30)
# plt.ylim([0, 200])
# l = None
