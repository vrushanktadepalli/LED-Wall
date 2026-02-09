import os
import time

from PIL import Image, ImageSequence
from rpi_ws281x import Color

from env import HEIGHT, WIDTH, strip

# Matrix configuration


def resize_and_center_frame(frame):
    """Resize and center a frame on a black canvas matching matrix size."""
    aspect_ratio = frame.width / frame.height

    if aspect_ratio > (WIDTH / HEIGHT):
        new_width = WIDTH
        new_height = int(WIDTH / aspect_ratio)
    else:
        new_height = HEIGHT
        new_width = int(HEIGHT * aspect_ratio)

    frame = frame.resize((new_width, new_height), Image.LANCZOS).convert('RGB')

    canvas = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    x_offset = (WIDTH - new_width) // 2
    y_offset = (HEIGHT - new_height) // 2
    canvas.paste(frame, (x_offset, y_offset))

    return list(canvas.getdata())

def zigzag_order(pixels, width, height):
    """Map 2D pixels to zigzag 1D LED strip layout."""
    result = []
    for y in range(height):
        row = pixels[y * width:(y + 1) * width]
        if y % 2 == 0:
            result.extend(row)
        else:
            result.extend(row[::-1])
    return result

def display_frame(pixels):
    """Display a list of RGB tuples on the LED matrix."""
    for i, (r, g, b) in enumerate(pixels):
        strip.setPixelColor(i, Color(g, r, b))
    strip.show()

def load_gif_frames(gif_path):
    """Extract and process all frames from a GIF."""
    img = Image.open(gif_path)
    frames = []

    for frame in ImageSequence.Iterator(img):
        processed = resize_and_center_frame(frame)
        zigzag = zigzag_order(processed, WIDTH, HEIGHT)
        frames.append(zigzag)

    return frames

def display_gif(gif_path, frame_duration=0.1):
    """Display a GIF file on the LED matrix."""
    frames = load_gif_frames(gif_path)
    print(f"Displaying GIF: {os.path.basename(gif_path)} with {len(frames)} frames")
        
    loops = int(max(5 / frame_duration, len(frames)))  # Play for at least 5 seconds
    print(f"Looping GIF for approximately {loops * frame_duration:.1f} seconds")
    for i in range(loops):
        display_frame(frames[i % len(frames)])
        time.sleep(frame_duration)

def cycle_gifs(folder):
    """Cycle through all GIFs in a folder."""
    gif_files = [f for f in os.listdir(folder) if f.lower().endswith('.gif')]
    print(f"Found {len(gif_files)} GIF(s) in folder: {folder}")
    
    for gif_file in gif_files:
        gif_path = os.path.join(folder, gif_file)
        display_gif(gif_path)

if __name__ == "__main__":
    try:
        while True:
            cycle_gifs('/home/pi/proj/gifs')  # Folder containing .gif files
    except KeyboardInterrupt:
        print("Program interrupted.")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
    
