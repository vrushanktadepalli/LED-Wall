from env import *
from utils import *

def main():
    set_brightness(100)
    gifs_show.display_gif(gif("supercoolgif.gif"))
    set_brightness(60)
    gifs_show.display_gif(gif("supercoolgif.gif"))
    set_brightness(170)
    gifs_show.display_gif(gif("supercoolgif.gif"))
    set_brightness(10)
    gifs_show.display_gif(gif("supercoolgif.gif"))
    

run_forever(main)