import math
import time

from env import HEIGHT, WIDTH, strip
from rpi_ws281x import Color

DEFAULT_COLOR = (255, 255, 255)
# Font dictionary (minimal example, complete it as needed)
# 5x7 Font for LED matrix in Python (dictionary format)
FONT = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    '!': [0x00, 0x00, 0x5F, 0x00, 0x00],
    '"': [0x00, 0x03, 0x00, 0x03, 0x00],
    '#': [0x14, 0x7F, 0x14, 0x7F, 0x14],
    '$': [0x24, 0x2A, 0x7F, 0x2A, 0x12],
    '%': [0x23, 0x13, 0x08, 0x64, 0x62],
    '&': [0x36, 0x49, 0x55, 0x22, 0x50],
    "'": [0x00, 0x05, 0x03, 0x00, 0x00],
    '(': [0x00, 0x1C, 0x22, 0x41, 0x00],
    ')': [0x00, 0x41, 0x22, 0x1C, 0x00],
    '*': [0x14, 0x08, 0x3E, 0x08, 0x14],
    '+': [0x08, 0x08, 0x3E, 0x08, 0x08],
    ',': [0x00, 0x50, 0x30, 0x00, 0x00],
    '-': [0x08, 0x08, 0x08, 0x08, 0x08],
    '.': [0x00, 0x60, 0x60, 0x00, 0x00],
    '/': [0x20, 0x10, 0x08, 0x04, 0x02],
    '0': [0x3E, 0x51, 0x49, 0x45, 0x3E],
    '1': [0x00, 0x42, 0x7F, 0x40, 0x00],
    '2': [0x72, 0x49, 0x49, 0x49, 0x46],
    '3': [0x21, 0x41, 0x45, 0x4B, 0x31],
    '4': [0x18, 0x14, 0x12, 0x7F, 0x10],
    '5': [0x27, 0x45, 0x45, 0x45, 0x39],
    '6': [0x3C, 0x4A, 0x49, 0x49, 0x30],
    '7': [0x01, 0x71, 0x09, 0x05, 0x03],
    '8': [0x36, 0x49, 0x49, 0x49, 0x36],
    '9': [0x06, 0x49, 0x49, 0x29, 0x1E],
    ':': [0x00, 0x36, 0x36, 0x00, 0x00],
    ';': [0x00, 0x56, 0x36, 0x00, 0x00],
    '<': [0x08, 0x14, 0x22, 0x41, 0x00],
    '=': [0x14, 0x14, 0x14, 0x14, 0x14],
    '>': [0x00, 0x41, 0x22, 0x14, 0x08],
    '?': [0x02, 0x01, 0x59, 0x09, 0x06],
    '@': [0x3E, 0x41, 0x5D, 0x55, 0x1E],
    'A': [0x7E, 0x09, 0x09, 0x09, 0x7E],
    'B': [0x7F, 0x49, 0x49, 0x49, 0x36],
    'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
    'D': [0x7F, 0x41, 0x41, 0x22, 0x1C],
    'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
    'F': [0x7F, 0x09, 0x09, 0x09, 0x01],
    'G': [0x3E, 0x41, 0x49, 0x49, 0x7A],
    'H': [0x7F, 0x08, 0x08, 0x08, 0x7F],
    'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
    'J': [0x20, 0x40, 0x41, 0x3F, 0x01],
    'K': [0x7F, 0x08, 0x14, 0x22, 0x41],
    'L': [0x7F, 0x40, 0x40, 0x40, 0x40],
    'M': [0x7F, 0x02, 0x04, 0x02, 0x7F],
    'N': [0x7F, 0x02, 0x04, 0x08, 0x7F],
    'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
    'P': [0x7F, 0x09, 0x09, 0x09, 0x06],
    'Q': [0x3E, 0x41, 0x51, 0x21, 0x5E],
    'R': [0x7F, 0x09, 0x19, 0x29, 0x46],
    'S': [0x26, 0x49, 0x49, 0x49, 0x32],
    'T': [0x01, 0x01, 0x7F, 0x01, 0x01],
    'U': [0x3F, 0x40, 0x40, 0x40, 0x3F],
    'V': [0x0F, 0x30, 0x40, 0x30, 0x0F],
    'W': [0x3F, 0x40, 0x38, 0x40, 0x3F],
    'X': [0x63, 0x14, 0x08, 0x14, 0x63],
    'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
    'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
    'a': [0x20, 0x54, 0x54, 0x54, 0x78],
    'b': [0x7F, 0x48, 0x44, 0x44, 0x38],
    'c': [0x38, 0x44, 0x44, 0x44, 0x20],
    'd': [0x38, 0x44, 0x44, 0x48, 0x7F],
    'e': [0x38, 0x54, 0x54, 0x54, 0x18],
    'f': [0x08, 0x7E, 0x09, 0x01, 0x02],
    'g': [0x0C, 0x52, 0x52, 0x52, 0x3E],
    'h': [0x7F, 0x08, 0x04, 0x04, 0x78],
    'i': [0x00, 0x44, 0x7D, 0x40, 0x00],
    'j': [0x20, 0x40, 0x44, 0x3D, 0x00],
    'k': [0x7F, 0x10, 0x28, 0x44, 0x00],
    'l': [0x00, 0x41, 0x7F, 0x40, 0x00],
    'm': [0x7C, 0x04, 0x18, 0x04, 0x78],
    'n': [0x7C, 0x08, 0x04, 0x04, 0x78],
    'o': [0x38, 0x44, 0x44, 0x44, 0x38],
    'p': [0x7C, 0x14, 0x14, 0x14, 0x08],
    'q': [0x08, 0x14, 0x14, 0x18, 0x7C],
    'r': [0x7C, 0x08, 0x04, 0x04, 0x08],
    's': [0x48, 0x54, 0x54, 0x54, 0x20],
    't': [0x04, 0x3F, 0x44, 0x40, 0x20],
    'u': [0x3C, 0x40, 0x40, 0x20, 0x7C],
    'v': [0x1C, 0x20, 0x40, 0x20, 0x1C],
    'w': [0x3C, 0x40, 0x30, 0x40, 0x3C],
    'x': [0x44, 0x28, 0x10, 0x28, 0x44],
    'y': [0x0C, 0x50, 0x50, 0x50, 0x3C],
    'z': [0x44, 0x64, 0x54, 0x4C, 0x44]
}


def zigzag_index(x, y):
    if y % 2 == 0:
        return y * WIDTH + x
    else:
        return y * WIDTH + (WIDTH - 1 - x)

def draw_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        strip.setPixelColor(zigzag_index(x, y), Color(*color))

def clear():
    for i in range(WIDTH * HEIGHT):
        strip.setPixelColor(i, Color(0, 0, 0))

def render_frame(frame):
    clear()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            draw_pixel(x, y, frame[y][x])
    strip.show()

def make_text_bitmap(text):
    bitmap = [[0 for _ in range(len(text)*6)] for _ in range(7)]
    for idx, char in enumerate(text):
        columns = FONT.get(char, FONT[' '])
        for col in range(5):
            byte = columns[col]
            for row in range(7):
                if byte & (1 << row):
                    bitmap[row][idx*6 + col] = 1
    return bitmap

def apply_color(bitmap, color):
    return [[color if pixel else (0, 0, 0) for pixel in row] for row in bitmap]

def scroll_left(text, color=DEFAULT_COLOR, speed=0.112):
    '''PLays a Text scrolling Left'''
    bitmap = make_text_bitmap(text)

    # Vertically pad bitmap to fit HEIGHT
    vertical_pad = HEIGHT - len(bitmap)
    top_pad = vertical_pad // 2
    bottom_pad = vertical_pad - top_pad
    padded_bitmap = [[0] * len(bitmap[0]) for _ in range(top_pad)] + bitmap + [[0] * len(bitmap[0]) for _ in range(bottom_pad)]

    # Horizontally pad each row
    padded = [[0]*WIDTH + row + [0]*WIDTH for row in padded_bitmap]
    total_width = len(padded[0])

    for shift in range(total_width - WIDTH + 1):
        frame = []
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                pixel_on = padded[y][x + shift]
                row.append(color if pixel_on else (0, 0, 0))
            frame.append(row)
        render_frame(frame)
        time.sleep(speed)

def scroll_right(text, color=DEFAULT_COLOR, speed=0.112):
    '''PLays a Text scrolling Right'''
    bitmap = make_text_bitmap(text)
    
    vertical_pad = HEIGHT - len(bitmap)
    top_pad = vertical_pad // 2
    bottom_pad = vertical_pad - top_pad
    padded_bitmap = [[0]*len(bitmap[0]) for _ in range(top_pad)] + bitmap + [[0]*len(bitmap[0]) for _ in range(bottom_pad)]

    padded = [[0]*WIDTH + row + [0]*WIDTH for row in padded_bitmap]
    total_width = len(padded[0])

    for shift in range(total_width - WIDTH, -1, -1):
        frame = []
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                pixel_on = padded[y][x + shift]
                row.append(color if pixel_on else (0, 0, 0))
            frame.append(row)
        render_frame(frame)
        time.sleep(speed)

def scroll_up(text, color=DEFAULT_COLOR, speed=0.112):
    '''PLays a Text scrolling Up'''
    bitmap = make_text_bitmap(text)
    text_height = len(bitmap)
    text_width = len(bitmap[0]) if bitmap else 0

    # Center horizontally
    x_offset = max((WIDTH - text_width) // 2, 0)

    # Padding: HEIGHT above and HEIGHT below
    padded_height = text_height + 2 * HEIGHT
    padded = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(padded_height)]

    # Paste bitmap at row = HEIGHT (so it's off-screen at first)
    for y in range(text_height):
        for x in range(text_width):
            if bitmap[y][x]:
                padded[y + HEIGHT][x + x_offset] = color

    # Scroll through entire padded area
    for shift in range(padded_height - HEIGHT + 1):
        frame = [
            [padded[y + shift][x] for x in range(WIDTH)]
            for y in range(HEIGHT)
        ]
        render_frame(frame)
        time.sleep(speed)

def scroll_down(text, color=DEFAULT_COLOR, speed=0.112):
    '''PLays a Text scrolling Down'''
    bitmap = make_text_bitmap(text)
    text_height = len(bitmap)
    text_width = len(bitmap[0]) if bitmap else 0

    # Center horizontally
    x_offset = max((WIDTH - text_width) // 2, 0)

    # Padding: HEIGHT above and HEIGHT below
    padded_height = text_height + 2 * HEIGHT
    padded = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(padded_height)]

    # Paste bitmap at top (HEIGHT rows down from the top so it scrolls in)
    for y in range(text_height):
        for x in range(text_width):
            if bitmap[y][x]:
                padded[y + HEIGHT][x + x_offset] = color

    # Scroll from top (i.e., padded_height - HEIGHT) down to 0
    for shift in reversed(range(padded_height - HEIGHT + 1)):
        frame = [
            [padded[y + shift][x] for x in range(WIDTH)]
            for y in range(HEIGHT)
        ]
        render_frame(frame)
        time.sleep(speed)

def blink_text(text, color=DEFAULT_COLOR, blink_times=5, on_duration=0.4, off_duration=0.2):
    '''PLays a Text blinking'''
    bitmap = make_text_bitmap(text)
    text_height = len(bitmap)
    text_width = len(bitmap[0]) if bitmap else 0

    x_offset = max((WIDTH - text_width) // 2, 0)
    y_offset = max((HEIGHT - text_height) // 2, 0)

    for _ in range(blink_times):
        # Frame ON
        frame_on = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for y in range(text_height):
            for x in range(text_width):
                if bitmap[y][x]:
                    frame_on[y + y_offset][x + x_offset] = color
        render_frame(frame_on)
        time.sleep(on_duration)

        # Frame OFF
        frame_off = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]
        render_frame(frame_off)
        time.sleep(off_duration)

def typewriter_text(text, color=DEFAULT_COLOR, speed=0.1):
    '''PLays a Text with a typewriter effect'''
    bitmap = make_text_bitmap(text)
    frame = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    text_height = len(bitmap)
    text_width = len(bitmap[0])

    y_offset = max((HEIGHT - text_height) // 2, 0)
    x_offset = max((WIDTH - text_width) // 2, 0)

    for col in range(text_width):
        for y in range(text_height):
            if bitmap[y][col]:
                x = x_offset + col
                if 0 <= x < WIDTH:
                    frame[y + y_offset][x] = color
        render_frame(frame)
        time.sleep(speed)
    time.sleep(0.4)

def wave_text(text, color=DEFAULT_COLOR, delay=0.06, amplitude=2, wavelength=2, cycles=3):
    '''PLays a Text with a wave effect'''
    char_height = 7
    char_width = 6  # 5 + 1 space
    bitmap = make_text_bitmap(text)  # Returns 7 x W bitmap
    text_width = len(bitmap[0])
    num_chars = text_width // char_width
    start_x = (WIDTH - text_width) // 2

    phase = 0
    cycle_length = 2 * math.pi  # One full sine wave
    total_frames = int((cycles * cycle_length) / 0.3)  # Adjust for step size below

    for _ in range(total_frames):
        frame = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]

        for i in range(num_chars):
            char_offset = int(amplitude * math.sin((i / wavelength) + phase))

            for y in range(char_height):
                for x in range(char_width):
                    bitmap_y = y
                    bitmap_x = i * char_width + x

                    if bitmap[bitmap_y][bitmap_x]:
                        screen_x = start_x + i * char_width + x
                        screen_y = (HEIGHT - char_height) // 2 + y + char_offset

                        if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
                            frame[screen_y][screen_x] = color

        render_frame(frame)
        time.sleep(delay)
        phase += 0.5

def display_text(text, color=DEFAULT_COLOR):
    """
    Display the given text
    """
    bitmap = make_text_bitmap(text)

    # Vertically pad to center
    vertical_pad = HEIGHT - len(bitmap)
    top_pad = vertical_pad // 2
    bottom_pad = vertical_pad - top_pad
    padded_bitmap = (
        [[0] * len(bitmap[0]) for _ in range(top_pad)]
        + bitmap
        + [[0] * len(bitmap[0]) for _ in range(bottom_pad)]
    )

    # If text is narrower than the LED matrix, center it horizontally
    text_width = len(padded_bitmap[0])
    if text_width < WIDTH:
        horizontal_pad = WIDTH - text_width
        left_pad = horizontal_pad // 2
        right_pad = horizontal_pad - left_pad
        padded_bitmap = [
            [0] * left_pad + row + [0] * right_pad
            for row in padded_bitmap
        ]
    else:
        # If text is too wide, crop to fit the display
        padded_bitmap = [
            row[:WIDTH] for row in padded_bitmap
        ]

    # Render to the LED matrix
    frame = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            pixel_on = padded_bitmap[y][x]
            row.append(color if pixel_on else (0, 0, 0))
        frame.append(row)

    render_frame(frame)
if __name__ == "__main__":
    try:
        while True:
            scroll_left("Left", color=(255, 0, 0), speed=0.07)
            scroll_right("Right", color=(0, 255, 0), speed=0.07)
            scroll_up("Up", color=(0, 0, 255), speed=0.2)
            scroll_down("Down", color=(255, 255, 0), speed=0.2)
            blink_text("Blink", color=(0, 255, 255))
            typewriter_text("Type", color=(255, 0, 255))
            wave_text("Wave", color=(255, 127, 0))
            display_text("H3110")
    except KeyboardInterrupt:
        clear()
        strip.show()
