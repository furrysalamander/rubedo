# import asyncio
# import aiohttp
import requests

# HOST = 'fluiddpi.local'
HOST = 'http://192.168.1.113'
GCODE_ENDPOINT = '/printer/gcode/script'
OBJECTS_ENDPOINT = '/printer/objects/query'

# Helper function to automatically generate the coordinate strings
# for G0 commands.
def format_move(x: float = None, y: float = None, z: float = None, f: float = None):
    def format_string(value, prefix):
        return f" {prefix}{value}" if value is not None else ""
    return "".join(format_string(value, prefix) for value, prefix in [(x, "x"), (y, "y"), (z, "z"), (f, "f")])


def move_absolute(x: float = None, y: float = None, z: float = None, f: float = None):
    return send_gcode(f"""
    G90
    G0{format_move(x, y, z, f)}
    """)


def move_relative(x: float = None, y: float = None, z: float = None, f: float = None):
    return send_gcode(f"""
    G91
    G0{format_move(x, y, z, f)}
    """)


async def send_gcode(gcode: str):
    async with aiohttp.ClientSession() as session:
        json_data = {
            "script": gcode
        }
        async with session.post(HOST + GCODE_ENDPOINT, json=json_data) as resp:
            return await resp.json()


def send_gcode(gcode: str):
    json_data = {
        "script": gcode
    }
    resp = requests.post(HOST + GCODE_ENDPOINT, json=json_data)
    return resp.json()


def home():
    return send_gcode('G28')


def has_homed():
    resp = requests.get(HOST + OBJECTS_ENDPOINT, params="toolhead")
    result = resp.json()["result"]
    return result["status"]["toolhead"]["homed_axes"] == "xyz"

def do_initialization_routine():
    # if not has_homed():
        # print("Homing")
        # home()
        # print("Quad Gantry Level")
        # send_gcode("QUAD_GANTRY_LEVEL")
        print("Rehoming Z")
        send_gcode("G28 Z")

def main():
    do_initialization_routine()
    print("Finished initializing")
    
    # move_absolute(150, 150, 16, 1000000)
    # move_absolute(10, 10, 20, 1000000)
    # move_absolute(150, 150, 16, 1000000)
    print("Done")


if __name__ == "__main__":
    main()

# start at x=45, y=305, end at x=109 (leaving 8mm off the start and end for now)
