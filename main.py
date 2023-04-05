#!/usr/bin/python3
from processing import *
from analysis import pa_score_from_video_file
from pattern_info import PatternInfo
from record import record_pattern
from pa_result import PaResult
from pa import *

import klipper.gcode as g

import tempfile
from pprint import pprint


# This will print a calibrated + control pattern and measure the % improvement after tuning
VALIDATE_RESULTS = True


PRINT_START = f"""
M104 S180; preheat nozzle while waiting for build plate to get to temp
M140 S{BUILD_PLATE_TEMPERATURE};
G28
M190 S{BUILD_PLATE_TEMPERATURE};
QUAD_GANTRY_LEVEL
CLEAN_NOZZLE
G28 Z
M109 S{HOTEND_TEMPERATURE};
"""

def generate_pa_results_for_pattern(pattern_info: PatternInfo)-> list[PaResult]:
    results = []

    # Hardcoding a buffer distance of 3mm here for now.  Adjust if needed.
    with tempfile.TemporaryDirectory("pa_videos") as dir:
        video_files = record_pattern(pattern_info, 3, dir)

        for video_file in video_files:
            results.append(
                pa_score_from_video_file(video_file)
            )
    return results


def main():
    calibration_pattern = PatternInfo(
        0, 0.06,
        30, 30,
        10,
        30, 4
    )

    
    # g.send_gcode(PRINT_START)
    g.send_gcode("CLEAN_NOZZLE")
    g.send_gcode(generate_pa_tune_gcode(calibration_pattern))
    g.wait_until_printer_at_location(FINISHED_X, FINISHED_Y)
    g.send_gcode("M104 S0; let the hotend cool")

    results = generate_pa_results_for_pattern(calibration_pattern)
        
    sorted_results = list(sorted(zip(results, calibration_pattern.pa_values), key=lambda x: x[0].score))
    sorted_results = list([(x.score, y) for x, y in sorted_results])

    best_pa_value = sorted_results[0][1]
    print()
    pprint(sorted_results)
    print()
    print(f"Recommended PA Value: {best_pa_value}, with a score of {sorted_results[0][0]}")
    print()
    g.send_gcode(f"SET_PRESSURE_ADVANCE ADVANCE={best_pa_value}")

    if not VALIDATE_RESULTS:
        return

    control = PatternInfo(
        0, 0,
        65, 30,
        10,
        30, 4
    )

    calibrated = PatternInfo(
        best_pa_value, best_pa_value,
        100, 30,
        10,
        30, 4
    )


    gcode = f"""
    M109 S{HOTEND_TEMPERATURE};
    CLEAN_NOZZLE
    """
    gcode += generate_pa_tune_gcode(control, False)
    gcode += generate_pa_tune_gcode(calibrated)
    g.send_gcode(gcode)
    g.send_gcode("M104 S0; let the hotend cool")
    g.wait_until_printer_at_location(FINISHED_X, FINISHED_Y)

    control_results = generate_pa_results_for_pattern(control)
    calibrated_results = generate_pa_results_for_pattern(calibrated)

    control_scores = list([x.score for x in control_results])
    calibrated_scores = list([x.score for x in calibrated_results])

    control_average = np.average(control_scores)
    calibrated_average = np.average(calibrated_scores)

    print("Control")
    pprint(control_scores)
    print("Calibrated")
    pprint(calibrated_scores)
    print()
    print(f"Average Control Score: {control_average}")
    print(f"Average Calibrated Score: {calibrated_average}")
    print()


if __name__=="__main__":
    main()
