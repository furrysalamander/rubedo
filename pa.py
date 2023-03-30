from pattern_info import PatternInfo
import klipper.gcode as g

BUILD_PLATE_TEMPERATURE = 110
HOTEND_TEMPERATURE = 255

def generate_pa_tune_gcode(info: PatternInfo):
    Z_HOP_HEIGHT = 0.75
    LAYER_HEIGHT = 0.25
    RETRACTION_DISTANCE = 0.5
    EXTRUSION_DISTANCE_PER_MM = 0.045899

    gcode = f"""
        G21 ; Millimeter units
        G90 ; Absolute XYZ
        M83 ; Relative E
        SET_VELOCITY_LIMIT ACCEL=3000 ACCEL_TO_DECEL=1500
        G92 E0 ;
        M106 S0 ; set fan speed to 0

        G1 X{info.start_x + info.line_length} Y{info.start_y} F30000 ; move to start position
        G1 Z{LAYER_HEIGHT} F300 ; move to layer height
        G91 ; switch to relative movements
        ; Print a bounding box to aid with removal and prime the extruder.
        G1 Y{info.num_lines * info.spacing} E{info.num_lines * info.spacing * EXTRUSION_DISTANCE_PER_MM} F3000;
        G1 X{-info.line_length} E{info.line_length * EXTRUSION_DISTANCE_PER_MM};
        G1 Y{-info.num_lines * info.spacing} E{info.num_lines * info.spacing * EXTRUSION_DISTANCE_PER_MM};
        G1 X{info.line_length} E{info.line_length * EXTRUSION_DISTANCE_PER_MM};
        G1 Z{Z_HOP_HEIGHT} Y{-info.spacing} E{-RETRACTION_DISTANCE} F300; retract and prepare to hop to first line location.
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
    M117 ; clear LCD message
    """
    return gcode

if __name__=="__main__":
    # FIXME: this stuff times out when it takes too long for the printer to respond... not sure
    # how to properly send commands and block until they're finished.  Can I poll for the printer
    # status?
    g.do_initialization_routine()
    g.send_gcode(f"""
    M104 S180; preheat nozzle while waiting for build plate to get to temp
    M190 S{BUILD_PLATE_TEMPERATURE};
    M109 S{HOTEND_TEMPERATURE};
    """)
    g.send_gcode("CLEAN_NOZZLE")
    g.send_gcode(
        generate_pa_tune_gcode(
            0, 0.1,
            30, 30,
            10,
            30, 4
        )
    )


# {% set BED = params.BED|default(99)|float %}
# {% set EXTRUDER = params.EXTRUDER|default(239)|float %}
# PRINT_START BED_TEMP={BED} EXTRUDER_TEMP={EXTRUDER}

# G21 ; Millimeter units
# G90 ; Absolute XYZ
# M83 ; Relative E
# SET_VELOCITY_LIMIT ACCEL=3000 ACCEL_TO_DECEL=1500
# G92 E0 ; 
# M106 S0 ; set fan speed to 0

# G1 X{start_x} Y{start_y} F30000      ; move to start position
# G1 Z0.25 F300                 ; move to layer height

# G91 ; switch to relative movements
# G1 E0.75 F1800           ; un-retract
# G1 X10 E0.45899 F300     ; print line part one
# G1 X20 E0.91798 F9000    ; print line part two
# G1 X10 E0.45899 F300     ; print line part three
# G1 E-0.75 F1800          ; retract
# G1 Z0.75 F300

# {% for i in range(0, 20) %}
# SET_PRESSURE_ADVANCE ADVANCE={i*0.005} ; set Pressure Advance
# M117 Testing Pressure Advance at: {i*0.005}
# G1 X-40 Y4 F30000        ; move to start position
# G1 Z-0.75 F300           ; move to layer height
# G1 E0.75 F1800           ; un-retract
# G1 X10 E0.45899 F300     ; print line part one
# G1 X20 E0.91798 F9000    ; print line part two
# G1 X10 E0.45899 F300     ; print line part three
# G1 E-0.75 F1800          ; retract
# G1 Z0.75 F300            ; Move above layer height  
# {% endfor %}

# PRINT_END

"""
[gcode_macro PA_CAL]
# Pressure Advance Simple Test macro, using .4mm nozzle.
# Usage: PA_CAL BED=100 EXTRUDER=240
# First prints a line with current set PA, then prints 20 line segments
# starting with 0 PA, increasing each line by 0.005.

# [gcode_macro CLEAN_NOZZLE]
# variable_start_x: 130
# variable_start_y: 350
# variable_start_z: 2
# variable_wipe_dist: -50
# variable_wipe_qty: 5
# variable_wipe_spd: 200
# variable_raise_distance: 10

# gcode:
#  {% if "xyz" not in printer.toolhead.homed_axes %}
#    G28
#  {% endif %}
 
#  G90                                            ; absolute positioning
#  ## Move nozzle to start position
#  G1 X{start_x} Y{start_y} F6000
#  G1 Z{start_z} F1500
variable_start_x: 10
variable_start_y: 200

gcode:
    {% set BED = params.BED|default(99)|float %}
    {% set EXTRUDER = params.EXTRUDER|default(239)|float %}
    PRINT_START BED_TEMP={BED} EXTRUDER_TEMP={EXTRUDER}

    G21 ; Millimeter units
    G90 ; Absolute XYZ
    M83 ; Relative E
    SET_VELOCITY_LIMIT ACCEL=3000 ACCEL_TO_DECEL=1500
    G92 E0 ; 
    M106 S0 ; set fan speed to 0

    G1 X{start_x} Y{start_y} F30000      ; move to start position
    G1 Z0.25 F300                 ; move to layer height

    G91 ; switch to relative movements
    G1 E0.75 F1800           ; un-retract
    G1 X10 E0.45899 F300     ; print line part one
    G1 X20 E0.91798 F9000    ; print line part two
    G1 X10 E0.45899 F300     ; print line part three
    G1 E-0.75 F1800          ; retract
    G1 Z0.75 F300

    {% for i in range(0, 20) %}
      SET_PRESSURE_ADVANCE ADVANCE={i*0.005} ; set Pressure Advance
      M117 Testing Pressure Advance at: {i*0.005}
      G1 X-40 Y4 F30000        ; move to start position
      G1 Z-0.75 F300           ; move to layer height
      G1 E0.75 F1800           ; un-retract
      G1 X10 E0.45899 F300     ; print line part one
      G1 X20 E0.91798 F9000    ; print line part two
      G1 X10 E0.45899 F300     ; print line part three
      G1 E-0.75 F1800          ; retract
      G1 Z0.75 F300            ; Move above layer height  
    {% endfor %}

    PRINT_END


# gcode:
#     {% set BED = params.BED|default(99)|float %}
#     {% set EXTRUDER = params.EXTRUDER|default(239)|float %}
#     PRINT_START BED_TEMP={BED} EXTRUDER_TEMP={EXTRUDER}

#     G21 ; Millimeter units
#     G90 ; Absolute XYZ
#     M83 ; Relative E
#     SET_VELOCITY_LIMIT ACCEL=3000 ACCEL_TO_DECEL=1500
#     G92 E0 ; 
#     M106 S0 ; set fan speed to 0

#     G1 X{start_x} Y{start_y} F30000      ; move to start position
#     G1 Z0.25 F300                 ; move to layer height

#     G91 ; switch to relative movements
#     G1 E0.75 F1800           ; un-retract
#     G1 X20 E0.91798 F300     ; print line part one
#     G1 X40 E1.83596 F9000    ; print line part two
#     G1 X20 E0.91798 F300     ; print line part three
#     G1 E-0.75 F1800          ; retract
#     G1 Z0.75 F300

#     {% for i in range(0, 20) %}
#       SET_PRESSURE_ADVANCE ADVANCE={i*0.005} ; set Pressure Advance
#       M117 Testing Pressure Advance at: {i*0.005}
#       G1 X-80 Y5 F30000        ; move to start position
#       G1 Z-0.75 F300           ; move to layer height
#       G1 E0.75 F1800           ; un-retract
#       G1 X20 E0.91798 F300     ; print line part one
#       G1 X40 E1.83596 F9000    ; print line part two
#       G1 X20 E0.91798 F300     ; print line part three
#       G1 E-0.75 F1800          ; retract
#       G1 Z0.75 F300            ; Move above layer height  
#     {% endfor %}

#     PRINT_END


    # SET_VELOCITY_LIMIT ACCEL=3000 ACCEL_TO_DECEL=1500
    # G92 E0 ; 
    # M106 S0 ; set fan speed to 0

    # G1 X120 Y70 F30000            ; move to start position
    # G1 Z0.25 F300                 ; move to layer height
    # G1 E0.75 F1800                ; un-retract
    # G1 X140 Y70 E0.91798 F300     ; print line part one
    # G1 X180 Y70 E1.83596 F9000    ; print line part two
    # G1 X200 Y70 E0.91798 F300     ; print line part three
    # G1 E-0.75 F1800               ; retract
    # G1 Z1 F300                    ; Move above layer height  

    # {% for i in range(0, 20) %}
    #   SET_PRESSURE_ADVANCE ADVANCE={i*0.005} ; set Pressure Advance
    #   M117 Testing Pressure Advance at: {i*0.005}
    #   G1 X120 Y{100+(5*i)} F30000            ; move to start position
    #   G1 Z0.25 F300                          ; move to layer height
    #   G1 E0.75 F1800                         ; un-retract
    #   G1 X140 Y{100+(5*i)} E0.91798 F300     ; print line part one
    #   G1 X180 Y{100+(5*i)} E1.83596 F9000    ; print line part two
    #   G1 X200 Y{100+(5*i)} E0.91798 F300     ; print line part three
    #   G1 E-0.75 F1800                        ; retract
    #   G1 Z1 F300                             ; Move above layer height  
    # {% endfor %}

    # PRINT_END
"""

