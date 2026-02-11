import os
from typing import Callable

from rpi_ws281x import Color, PixelStrip

WIDTH: int = 32
HEIGHT: int = 16
PIXEL_COUNT: int= WIDTH * HEIGHT

# LED configuration
LED_PIN: int = 12
LED_BRIGHTNESS: int = 170
LED_COUNT: int = PIXEL_COUNT

# Initialize LED strip
strip: PixelStrip = PixelStrip(LED_COUNT, LED_PIN, brightness=LED_BRIGHTNESS)
strip.begin()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

_image_folder = os.path.join(ASSETS_DIR, "images")
_video_folder = os.path.join(ASSETS_DIR, "videos")
_gif_folder = os.path.join(ASSETS_DIR, "gifs")

def image(file: str) -> str:
    return os.path.join(_image_folder, file)

def video(file: str) -> str:
    return os.path.join(_video_folder, file)

def gif(file: str) -> str:
    return os.path.join(_gif_folder, file)

def clear_leds() -> None:
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def set_brightness(value: int) -> None:
    value = max(0, min(255, value))
    strip.setBrightness(value)
    strip.show()

set_brightness(LED_BRIGHTNESS)

def run_once(fn: Callable) -> None:
    try:
        fn()
        clear_leds()
    except KeyboardInterrupt:
        clear_leds()

def run_forever(fn: Callable) -> None:
    try:
        while True:
            fn()
    except KeyboardInterrupt:
        clear_leds()