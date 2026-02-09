from env import *
from utils import *


def main():

    display_image(image("windows.png"))

    display_video(video("badapple.mp4"))

    display_gif(gif("supercool.gif"))

run_forever(main)