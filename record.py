from klipper.gcode import *
from pattern_info import PatternInfo
import numpy as np
import subprocess
import time

# TODO: Populate all of these.
CAMERA_OFFSET_X = 0
CAMERA_OFFSET_Y = 0

CAMERA_FOV_X = 0
CAMERA_FOV_Y = 0

LASER_FOCUS_HEIGHT = 17.86

ffmpeg_cmd = [
    "ffmpeg",
    "-f",
    "v4l2",
    "-framerate",
    "30",
    "-video_size",
    "1280x720",
    "-input_format",
    "mjpeg",
    "-i",
    "/dev/video0",
    ]


# TODO: make this return a list of files that are saved
# TODO: make this save to a unique folder each run (maybe this should be passed in?)
def record_pattern(info: PatternInfo, buffer_distance: float) -> list:
    send_gcode("STATUS_OFF") # Turn off LEDs
    send_gcode("LASER_ON") # Turn on line laser

    y_values = np.ndarray(info.lines_start_y) + CAMERA_OFFSET_Y
    scan_start_x = info.start_x + buffer_distance + CAMERA_OFFSET_X
    scan_length = info.line_length - buffer_distance

    time.sleep(2)
    for index, y_value in enumerate(y_values):
        move_absolute(scan_start_x, y_value, LASER_FOCUS_HEIGHT, 30000)
        # start recording
        with subprocess.Popen(ffmpeg_cmd + [f"sample_data2/line{index}.mp4"]) as ffmpeg:
            # move_relative(64, f=600)
            time.sleep(0.5)
            print(move_relative(scan_length, f=600))
            
            # Total hack here... I need to not hardcode this.
            # We should be able to compute this programatically relatively easily.
            time.sleep(5)

            ffmpeg.terminate()
            time.sleep(0.5)
        # stop recording
        # print(move_relative(-34, 4, f=18000))
        time.sleep(1)


# start at x=45, y=250, end at x=73 (leaving 8mm off the start and end for now)
def main():

    # record_pattern()
    pass

if __name__=="__main__":
    main()
