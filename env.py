import os
from typing import Callable

from rpi_ws281x import Color, PixelStrip

WIDTH = 32
HEIGHT = 16
PIXEL_COUNT = WIDTH * HEIGHT

# LED configuration
LED_PIN = 12
LED_BRIGHTNESS = 170
LED_COUNT = PIXEL_COUNT

# Initialize LED strip
strip: PixelStrip = PixelStrip(LED_COUNT, LED_PIN, brightness=LED_BRIGHTNESS)
strip.begin()

image_folder = '/home/pi/proj/images' 
video_folder = '/home/pi/proj/videos'
gif_folder = '/home/pi/proj/gifs'
image = lambda file: os.path.join(image_folder, file)
video = lambda file: os.path.join(video_folder, file)
gif = lambda file: os.path.join(gif_folder, file)

def clear_leds() -> None:
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
def set_brightness(value: int) -> None:
    value = max(0, min(255, value))
    strip.setBrightness(value)
    strip.show()
set_brightness(LED_BRIGHTNESS)
def run_forever(fn: Callable) -> None:
    try:
        while True:
            fn()
    except KeyboardInterrupt:
        clear_leds()