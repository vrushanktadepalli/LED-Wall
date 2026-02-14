import os
import time

from PIL import Image, ImageSequence
from rpi_ws281x import Color

from env import HEIGHT, WIDTH, clear_leds, gif, strip

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

def display_gif(gif_name, frame_duration=0.1):
    """Display a GIF file on the LED matrix."""
    gif_path = gif(gif_name)
    frames = load_gif_frames(gif_path)
    print(f"Displaying GIF: {os.path.basename(gif_path)} with {len(frames)} frames")
        
    loops = int(max(5 / frame_duration, len(frames)))  # Play for at least 5 seconds
    print(f"Looping GIF for approximately {loops * frame_duration:.1f} seconds")
    for i in range(loops):
        display_frame(frames[i % len(frames)])
        time.sleep(frame_duration)

def cycle_gifs(folder=os.path.join(os.path.dirname(__file__), '..', 'assets', 'gifs')):
    """Cycle through all GIFs in a folder."""
    gif_files = [f for f in os.listdir(folder) if f.lower().endswith('.gif')]
    print(f"Found {len(gif_files)} GIF(s) in folder: {folder}")
    
    for gif_file in gif_files:
        display_gif(gif_file)

def main():
    try:
        while True:
            cycle_gifs()  # Folder containing .gif files
    except KeyboardInterrupt:
        print("Program interrupted.")
        clear_leds()

if __name__ == "__main__":
    main()
    
