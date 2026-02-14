from env import *
from utils import *

def main():

    display_image("windows.png")
    display_video("badapple.mp4")
    display_gif("supercool.gif")

    cycle_gifs()
    cycle_images()
    cycle_videos()

    matrix_rain()
    dvd5px()
    spiral()

    scroll_down("DOWN")
    scroll_up("UP")
    scroll_left("LEFT")
    scroll_right("RIGHT")
    wave_text("WAVE")
    typewriter_text("WRITE")
    blink_text("BLINK")
    display_text("NONE")


run_forever(main)