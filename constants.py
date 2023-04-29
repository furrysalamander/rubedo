# Connection details for communicating with the printer's moonraker API.
HOST = '192.168.1.114'
WS_PORT = 7125
GCODE_ENDPOINT = '/printer/gcode/script'
OBJECTS_ENDPOINT = '/printer/objects/query'

# This will print a calibrated + control pattern and measure the % improvement after tuning
VALIDATE_RESULTS = True

# Print settings
BUILD_PLATE_TEMPERATURE = 110
HOTEND_TEMPERATURE = 255
HOTEND_IDLE_TEMP = 200

# This is where the toolhead moves to indicate that it's done printing the PA pattern.
FINISHED_X = 30
FINISHED_Y = 250

# Any gcode you want to be sent before the pattern is printed.
# You could just have this call PRINT_START if you've configured
# that for your printer.
PRINT_START = f"""
M104 S180; preheat nozzle while waiting for build plate to get to temp
M140 S{BUILD_PLATE_TEMPERATURE};
G28
M190 S{BUILD_PLATE_TEMPERATURE};
QUAD_GANTRY_LEVEL
CLEAN_NOZZLE
G28 Z
M109 S{HOTEND_TEMPERATURE};
CLEAN_NOZZLE
"""

# Information about the USB camera mounted to the hotend.
VIDEO_DEVICE = "/dev/video2"
VIDEO_RESOLUTION = "1280x720"
FRAMERATE = "30"
# The camera's distance from the nozzle.
# This tells the recording code how to center the line within the camera's field of view.
# The offsets are in mm.
CAMERA_OFFSET_X = 28
CAMERA_OFFSET_Y = 50.2

# This is the height where the camera and laser are in focus.
LASER_FOCUS_HEIGHT = 17.86

# How the processing code finds the area of interest. Units are in pixels.
# The crop offsets specify the pixel that the box should be centered on.
CROP_X_OFFSET = 220
# In my case, the crop Y offset should be zero, but my offset Y value above is slightly off.
# You can kind of tweak these if you find that things aren't quite right.
CROP_Y_OFFSET = 11
# How big the area around the laser should be cropped to.
CROP_FRAME_SIZE_X = 45
CROP_FRAME_SIZE_Y = 60

# Sometimes ffmpeg is slow to close. If we start moving too early, 
# we might accidentally record stuff we don't want to.
# I would like to eliminate these eventually by improving the video recording code.
FFMPEG_START_DELAY = 0.5
FFMPEG_STOP_DELAY = 0.6

# Pressure Advance Pattern Configuration
# This changes how the gcode for the pressure advance pattern is generated.
# Only edit this if you need to.
Z_HOP_HEIGHT = 0.75
LAYER_HEIGHT = 0.25
RETRACTION_DISTANCE = 0.5
EXTRUSION_DISTANCE_PER_MM = 0.045899
BOUNDING_BOX_LINE_WIDTH = 0.4 # May need adjustment. 

# TODO: implement support for these.
# If we know the FOV, we can attach actual units
# to the values that are calculated.
# CAMERA_FOV_X = 0
# CAMERA_FOV_Y = 0

# These were used earlier on in development, but I need to re-implement 
# them, as the refactor I did removed the code that made them work.
# OUTPUT_GRAPH = False
# OUTPUT_FRAMES = True
# OUTPUT_HEIGHT_MAPS = False
