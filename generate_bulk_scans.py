from pprint import pprint
import klipper.gcode as g
from main import generate_pa_results_for_pattern, PRINT_START
from pa import *
from pa_result import PaResult
import pickle

def main():
    patterns: list[PatternInfo] = []
    for x in range(20, 286, 31):
        for y in range(80, 190, 45):
            patterns.append(
                PatternInfo(
                    0, 0.06,
                    x, y,
                    10,
                    30, 4
            ))

    # g.send_gcode(PRINT_START)
    # g.send_gcode("M109 S255")
    # g.send_gcode("CLEAN_NOZZLE")
    # for pattern in patterns:
    #     g.send_gcode(generate_pa_tune_gcode(pattern, False))
    # g.send_gcode("G90;")
    # g.send_gcode(f"G1 X{FINISHED_X} Y{FINISHED_Y} F30000")
    # g.wait_until_printer_at_location(FINISHED_X, FINISHED_Y)
    # g.send_gcode("M104 S0; let the hotend cool")

    pa_scans: list[PaResult] = []

    for pattern in patterns:
        pa_scans.extend(
            zip(pattern.pa_values,
            generate_pa_results_for_pattern(
                pattern
            ))
        )

    with open("matte_white_ambient_light.pkl", "wb") as f:
        pickle.dump(pa_scans, f)

    # results = generate_pa_results_for_pattern(calibration_pattern)
        
    # sorted_results = list(sorted(zip(results, calibration_pattern.pa_values), key=lambda x: x[0].score))
    # sorted_results = list([(x.score, y) for x, y in sorted_results])

    # best_pa_value = sorted_results[0][1]
    # print()
    # pprint(sorted_results)
    # print()
    # print(f"Recommended PA Value: {best_pa_value}, with a score of {sorted_results[0][0]}")
    # print()
    # g.send_gcode(f"SET_PRESSURE_ADVANCE ADVANCE={best_pa_value}")

if __name__=="__main__":
    main()
