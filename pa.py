#!/usr/bin/python3
from pattern_info import PatternInfo
from constants import *

def generate_pa_tune_gcode(info: PatternInfo, finished_printing=True):
    def gcode_relative_extrude_move(x=None, y=None):
        # Does not support diagonal moves
        if x is not None:
            move_str = f"X{x}"
            move_mag = abs(x)
        else:
            move_str = f"Y{y}"
            move_mag = abs(y)
        
        return f"G1 {move_str} E{move_mag * EXTRUSION_DISTANCE_PER_MM} F2000;"

    bounding_box_height = (len(info.pa_values) + 1) * info.spacing

    gcode = f"""
        G21 ; Millimeter units
        G90 ; Absolute XYZ
        M83 ; Relative E
        SET_VELOCITY_LIMIT ACCEL=3000 ACCEL_TO_DECEL=1500
        G92 E0 ;
        M106 S0 ; set fan speed to 0

        G1 X{info.start_x + info.line_length + BOUNDING_BOX_LINE_WIDTH} Y{info.start_y - info.spacing - BOUNDING_BOX_LINE_WIDTH} F30000 ; move to start position
        G1 Z{LAYER_HEIGHT} F300 ; move to layer height
        G91 ; switch to relative movements

        ; Print a bounding box to aid with removal and prime the extruder.
        G1 E{RETRACTION_DISTANCE * 2}
        {gcode_relative_extrude_move(y=bounding_box_height + BOUNDING_BOX_LINE_WIDTH * 2)}
        {gcode_relative_extrude_move(x=-(info.line_length + BOUNDING_BOX_LINE_WIDTH * 2))}
        {gcode_relative_extrude_move(y=-(bounding_box_height + BOUNDING_BOX_LINE_WIDTH * 2))}
        {gcode_relative_extrude_move(x=info.line_length + BOUNDING_BOX_LINE_WIDTH * 2)}
        G1 X{-BOUNDING_BOX_LINE_WIDTH} Y{BOUNDING_BOX_LINE_WIDTH}
        ; second bounding box loop
        {gcode_relative_extrude_move(y=bounding_box_height)}
        {gcode_relative_extrude_move(x=-info.line_length)}
        {gcode_relative_extrude_move(y=-bounding_box_height)}
        {gcode_relative_extrude_move(x=info.line_length)}

        G1 Z{Z_HOP_HEIGHT} E{-RETRACTION_DISTANCE} F300; retract and prepare to hop to first line location.
    """

    for pa_value in info.pa_values:
        # TODO: parameterize the extrusion values based on the layer height
        #
        # TODO: the lines could be printed in alternating directions to 
        #   eliminate the need for retractions and also decrease print time.
        gcode += f"""
            SET_PRESSURE_ADVANCE ADVANCE={pa_value} ; set Pressure Advance
            M117 Testing Pressure Advance at: {pa_value}
            G1 X-{info.line_length} Y{info.spacing} F30000        ; move to start position
            G1 Z{-Z_HOP_HEIGHT} F300           ; move to layer height
            G1 E{RETRACTION_DISTANCE} F1800           ; un-retract
            G1 X{info.line_length / 4} E{(info.line_length / 4) * EXTRUSION_DISTANCE_PER_MM} F300     ; print line part one
            G1 X{info.line_length / 2} E{(info.line_length / 2) * EXTRUSION_DISTANCE_PER_MM} F9000    ; print line part two
            G1 X{info.line_length / 4} E{(info.line_length / 4) * EXTRUSION_DISTANCE_PER_MM} F300     ; print line part three
            G1 E{-RETRACTION_DISTANCE} F1800          ; retract
            G1 Z{Z_HOP_HEIGHT} F300            ; Move above layer height 
        """
    gcode += """
    G1 Z5; move up 1mm
    M117
    """
    if finished_printing:
        gcode += f"""
        G90; switch back to absolute coordinates
        G1 X{FINISHED_X} Y{FINISHED_Y} Z20 F30000;
        """
    # print(gcode)
    return gcode


def main():
    # FIXME: this stuff times out when it takes too long for the printer to respond... not sure
    # how to properly send commands and block until they're finished.  Can I poll for the printer
    # status?
    gcode = f"""
    G28
    M104 S180; preheat nozzle while waiting for build plate to get to temp
    M190 S{BUILD_PLATE_TEMPERATURE};
    QUAD_GANTRY_LEVEL
    CLEAN_NOZZLE
    G28 Z
    M109 S{HOTEND_TEMPERATURE};
    """
    # PA Patterns
    control = PatternInfo(
        0, 0,
        30, 30,
        10,
        30, 4
    )
    normal_pattern = PatternInfo(
        0, 0.06,
        65, 30,
        10,
        30, 4
    )
    calibrated = PatternInfo(
        0.04, 0.04,
        100, 30,
        10,
        30, 4
    )


    gcode += generate_pa_tune_gcode(control)
    gcode += generate_pa_tune_gcode(normal_pattern)
    gcode += generate_pa_tune_gcode(calibrated)

    # Reset PA so I don't forget.
    gcode += """
    SET_PRESSURE_ADVANCE ADVANCE=0.04
    """

    with open("pa_patterns.gcode", "w") as f:
        f.write(gcode)


    


if __name__=="__main__":
    main()
