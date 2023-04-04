from klipper.gcode import *
from pattern_info import PatternInfo
import numpy as np
import subprocess
import time
from pathlib import Path

# TODO: Populate all of these.
CAMERA_OFFSET_X = 28
CAMERA_OFFSET_Y = 50.2

CAMERA_FOV_X = 0
CAMERA_FOV_Y = 0

LASER_FOCUS_HEIGHT = 17.86

ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-f",
    "v4l2",
    "-framerate",
    "30",
    "-video_size",
    "1280x720",
    "-input_format",
    "mjpeg",
    "-i",
    "/dev/video2",
    ]


# TODO: make this return a list of files that are saved
# TODO: make this save to a unique folder each run (maybe this should be passed in?)
def record_pattern(info: PatternInfo, buffer_distance: float, output_directory: str) -> list:
    send_gcode("STATUS_OFF") # Turn off LEDs
    send_gcode("LASER_ON") # Turn on line laser
    time.sleep(0.5)

    lines_start_y = info.lines_start_y()
    y_values = np.asarray(lines_start_y) + CAMERA_OFFSET_Y
    scan_start_x = info.start_x + buffer_distance + CAMERA_OFFSET_X
    scan_length = info.line_length - buffer_distance * 2
    scan_end_x = scan_start_x + scan_length

    video_files = []
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    for index, y_value in enumerate(y_values):
        move_absolute(scan_start_x, y_value, LASER_FOCUS_HEIGHT, 30000)
        wait_until_printer_at_location(scan_start_x, y_value)
        # start recording

        video_file = f"{output_directory}/line{index}.mp4"
        video_files.append(video_file)

        with subprocess.Popen(ffmpeg_cmd + [video_file]) as ffmpeg:
            time.sleep(0.5)
            print(move_absolute(scan_end_x, f=600))
            wait_until_printer_at_location(scan_end_x)

            # stop recording
            ffmpeg.terminate()
            time.sleep(0.6)

    send_gcode("LASER_OFF")
    return video_files

