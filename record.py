from klipper.gcode import *
import subprocess
import time

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

# start at x=45, y=250, end at x=73 (leaving 8mm off the start and end for now)
def main():
    
    send_gcode("STATUS_OFF")
    send_gcode("LASER_ON")
    move_absolute(40, 250, 17.86, 18000)
    time.sleep(2)
    for i in range(20):
        # start recording
        # with open('') as f:
        with subprocess.Popen(ffmpeg_cmd + [f"sample_data2/line{i}.mp4"]) as ffmpeg:
            # move_relative(64, f=600)
            time.sleep(0.5)
            print(move_relative(34, f=600))
            time.sleep(5)
            ffmpeg.terminate()
            time.sleep(0.5)
        # stop recording
        print(move_relative(-34, 4, f=18000))
        time.sleep(1)

if __name__=="__main__":
    main()
