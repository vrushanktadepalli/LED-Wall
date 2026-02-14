import os
import time

from PIL import Image
from rpi_ws281x import Color

from env import HEIGHT, WIDTH, clear_leds, image, strip

# Initialize LED strip

def increase_brightness(img, gamma=20):
    """Apply gamma correction to an image for non-linear brightness adjustment."""
    gamma_corrected = Image.new("RGB", img.size)
    inv_gamma = 1.0 / gamma
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            r_corr = int(255 * ((r / 255) ** inv_gamma))
            g_corr = int(255 * ((g / 255) ** inv_gamma))
            b_corr = int(255 * ((b / 255) ** inv_gamma))
            gamma_corrected.putpixel((x, y), (r_corr, g_corr, b_corr))
    return gamma_corrected

def process_image(image_path, width=WIDTH, height=HEIGHT, brightness_factor=1.5):
    """Resize, pad, brighten, and return pixel list."""
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((width, height), Image.LANCZOS)

    canvas = Image.new("RGB", (width, height), (0, 0, 0))
    x_offset = (width - img.width) // 2
    y_offset = (height - img.height) // 2
    canvas.paste(img, (x_offset, y_offset))

    bright_img = increase_brightness(canvas, brightness_factor)
    return list(bright_img.getdata())

def zigzag_order(pixels, width, height):
    """Reorder pixels in serpentine zigzag format."""
    zigzag = []
    for y in range(height):
        row = pixels[y * width:(y + 1) * width]
        zigzag.extend(row if y % 2 == 0 else row[::-1])
    return zigzag

def to_grb_color(r, g, b):
    return Color(g, r, b)

def display_image(image_name, delay_time=3):
    image_path = image(image_name)
    print(f"Displaying: {os.path.basename(image_path)}")
    pixels = process_image(image_path, brightness_factor=0.6)
    zigzag = zigzag_order(pixels, WIDTH, HEIGHT)
    for i, (r, g, b) in enumerate(zigzag):
        strip.setPixelColor(i, to_grb_color(r, g, b))
    strip.show()
    time.sleep(delay_time)

def cycle_images(folder=os.path.join(os.path.dirname(__file__), '..', 'assets', 'images'), delay_time=2):
    for fname in sorted(os.listdir(folder)):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            display_image(os.path.join(folder, fname), delay_time)

def main():
    image_folder = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')
    try:
        cycle_images(image_folder)
    except KeyboardInterrupt:
        print("Stopped.")
        clear_leds()

if __name__ == "__main__":
    main()
