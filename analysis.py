import numpy as np
from constants import *
from processing import *
from pa_result import PaResult

def brightest_average(pixel_values: np.ndarray):
    brightest_pixels = np.argsort(pixel_values)[-3:]
    line_brightest_x = CROP_FRAME_SIZE_X - np.average(brightest_pixels)
    return line_brightest_x


def weighted_average(pixel_values: np.ndarray):
    normalized_values = pixel_values / 255
    adjusted_values = normalized_values ** 100
    x_values = np.arange(adjusted_values.size)
    if adjusted_values.max() == 0:
        # FIXME: I need an appropriate solution for what to do if there are no non-zero values.
        return 70
    return CROP_FRAME_SIZE_X - np.average(x_values, weights=adjusted_values)


def first_non_zero(pixel_values: np.ndarray):
    try:
        return np.nonzero(pixel_values)[0][0]
    except:
        print()


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
    return algorithms["weighted_avg"](pixel_values)


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
    height_data: np.ndarray = np.ndarray((frame_count, CROP_FRAME_SIZE_Y))

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


def pa_score_from_video_file(video_file: str) -> PaResult:
    video_height_data = generate_height_data_from_video(video_file)

    # if OUTPUT_HEIGHT_MAPS:
    #     graph_height_map(video_height_data, f"height_maps/{Path(video_file).stem}.png")

    score = compute_score_from_heightmap(video_height_data)

    return PaResult(video_file, video_height_data, score)

