import os
import time

import cv2
import numpy as np
from rpi_ws281x import Color
from env import HEIGHT, WIDTH, strip
def resize_with_aspect_ratio(frame, target_width, target_height):
    h, w = frame.shape[:2]
    aspect_ratio = w / h

    if aspect_ratio > (target_width / target_height):
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    return cv2.resize(frame, (new_width, new_height))

def zigzag_index(x, y):
    """Convert (x, y) to LED index in zigzag layout (top-left origin)."""
    if y % 2 == 0:
        return y * WIDTH + x
    else:
        return y * WIDTH + (WIDTH - 1 - x)

def display_frame(frame):
    """Send a 32x16 image to the LED matrix."""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            b, g, r = frame[y, x]
            idx = zigzag_index(x, y)
            strip.setPixelColor(idx, Color(r, g, b))
    strip.show()

def play_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Error: Couldn't open video {path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized = resize_with_aspect_ratio(frame, WIDTH, HEIGHT)
        canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        y_offset = (HEIGHT - resized.shape[0]) // 2
        x_offset = (WIDTH - resized.shape[1]) // 2

        canvas[y_offset:y_offset + resized.shape[0], x_offset:x_offset + resized.shape[1]] = resized
        display_frame(canvas)

    cap.release()


def cycle_videos(video_folder):
    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith(".mp4")]
    if not video_files:
        print("No video files found in 'videos/' folder.")
        return
    
    for video in video_files:
        print(f"Playing {video}")
        play_video(os.path.join(video_folder, video))

def main():
    video_folder = "/home/pi/proj/videos"
    try:
        while True:
            cycle_videos(video_folder)
    except KeyboardInterrupt:
        print("Exiting videoshow.py")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

if __name__ == "__main__":
    main()